# downloader_checker.py v2.3.1

# This script is responsible for checking the availability of new videos and managing their download process. It utilizes the video_downloader module to perform the actual download, and it ensures that each video is only downloaded once by checking against a record of previously downloaded videos.

import time
import os
import logging
import random  # Importing random to introduce randomness in retry intervals
from typing import Any, Optional
from utils import sanitize_filename
from config_loader import load_config
from metadata_manager import MetadataManager

# 创建一个logger对象
logger = logging.getLogger(__name__)

config = load_config()

class DownloaderManager:

    def __init__(self, videos, downloader, config):
        """Initialize the DownloaderManager with videos to be downloaded, a downloader, and configuration.
        
        Parameters:
        - videos : list : A list of video information to be downloaded.
        - downloader : YTDownloader : An instance of YTDownloader to perform the actual download.
        - config : dict : Configuration parameters.
        """
        self.videos = videos
        self.downloader = downloader
        self.metadata_manager = MetadataManager(config)  # 创建MetadataManager的实例，并传递配置

    def should_download(self, video_info):
        """Determine if a video should be downloaded based on its title and metadata.
        
        Parameters:
        - video_info : dict : Information about the video to be downloaded.
        
        Returns:
        - bool : True if the video should be downloaded, False otherwise.
        """
        sanitized_title = sanitize_filename(video_info['title'])
        video_path = os.path.join(self.downloader.output_directory, sanitized_title + '.mp4')

        # Check if the file exists in the file system.
        file_exists = os.path.exists(video_path)

        # Check if metadata exists.
        metadata_exists = self.metadata_manager.query_metadata(video_info['id']) is not None

        return not (file_exists and metadata_exists)


    def store_video_metadata(self, video_info):
        """Store video metadata using MetadataManager."""
        sanitized_title = sanitize_filename(video_info['title'])
        video_path = os.path.join(self.downloader.output_directory, sanitized_title + '.mp4')
        metadata = {
            'id': video_info['id'],  # 假设 video_info 包含一个唯一的 'id' 字段
            'title': video_info['title'],
            'url': video_info['url'],
            'description': video_info['description'],
            'published_at': video_info.get('published_at', 'Unknown Date'),
            'video_path': video_path,
            'downloaded_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        self.metadata_manager.save_or_update_metadata(metadata)

    def check_and_download(self):
        downloaded_count = 0
        downloaded_titles = []  

        logger.info(f"Preparing to download {len(self.videos)} videos...")

        for video_url in self.videos:
            try:
                downloaded_title = self._download_single_video(video_url)  # Simplified download logic
                if downloaded_title:
                    downloaded_titles.append(downloaded_title)
                    downloaded_count += 1
            except Exception as e:
                logger.error(f"Failed to download video from {video_url}. Error: {e}.", exc_info=True)  # Logging more error info

        return downloaded_titles, downloaded_count
    
    def _download_single_video(self, video_url: str) -> Optional[str]:
        """Try downloading a single video and return the title if successful.
        Parameters:
        - video_url : str : URL of the video to be downloaded.
        
        Returns:
        - Optional[str] : Title of the downloaded video if successful, None otherwise.
        """
        retries = 0
        max_retries = config.get("MAX_DOWNLOAD_RETRIES", 3)  # Getting the value from config with a default

        while retries < max_retries:
            try:
                video_info = self.downloader.get_video_info(video_url)

                if self.should_download(video_info):
                    print(f"Downloading: {video_info['title']}")
                    self.downloader.download_video(video_url)
                    self.store_video_metadata(video_info)
                    logger.info(f"Successfully downloaded {video_info['title']}.")
                    return video_info['title']  # Return the title of the downloaded video

                sanitized_title = sanitize_filename(video_info['title'])
                print(f"Video {sanitized_title} already exists. Skipping download.")
                logger.info(f"Video {sanitized_title} already exists. Skipping download.")
                return None  # Return None if the video was not downloaded

            except Exception as e:
                logger.error(f"Error downloading video from {video_url}. Error: {e}. Retrying...")
                retries += 1
                if retries >= max_retries:
                    logger.error(f"Failed to download video from {video_url} after {retries} retries.")
                    return None  # Return None if the download failed after retries

                sleep_time = (retries + 1) * 5 + random.randint(1, 5)  # Adding randomness to the sleep time
                time.sleep(sleep_time)  # Exponential backoff with randomness