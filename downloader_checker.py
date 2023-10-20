# downloader_checker.py v2.2.1
# - Enhanced error handling in the check_and_download method.

import time
import os
import logging
from utils import sanitize_filename
from config_loader import load_config
from metadata_manager import MetadataManager

# 创建一个logger对象
logger = logging.getLogger(__name__)

config = load_config()

class DownloaderManager:

    def __init__(self, videos, downloader):
        self.videos = videos
        self.downloader = downloader
        self.metadata_manager = MetadataManager()  # 创建MetadataManager的实例

    def should_download(self, video_info):
        """Determine if a video should be downloaded based on its title and metadata."""
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
        downloaded_titles = []  # 新增：存储已下载视频的标题
        print(f"Preparing to download {len(self.videos)} videos...")
        logger.info(f"Preparing to download {len(self.videos)} videos...")

        for video_url in self.videos:
            retries = 0
            while retries < config["MAX_DOWNLOAD_RETRIES"]:
                try:
                    video_info = self.downloader.get_video_info(video_url)

                    if self.should_download(video_info):
                        print(f"Downloading: {video_info['title']}")
                        self.downloader.download_video(video_url)
                        self.store_video_metadata(video_info)
                        logger.info(f"Successfully downloaded {video_info['title']}.")
                        downloaded_count += 1
                        downloaded_titles.append(video_info['title'])  # 新增：将标题添加到列表
                        break  # Once successfully downloaded, break out of the retry loop
                    else:
                        sanitized_title = sanitize_filename(video_info['title'])
                        print(f"Video {sanitized_title} already exists. Skipping download.")
                        logger.info(f"Video {sanitized_title} already exists. Skipping download.")
                        break  # Video already exists, so no need to retry
                except Exception as e:
                    logger.error(f"Error downloading video from {video_url}. Error: {e}.")
                    retries += 1
                    if retries >= config["MAX_DOWNLOAD_RETRIES"]:
                        raise e
                    time.sleep((retries + 1) * 5)

        return downloaded_titles, downloaded_count  # 修改：返回已下载视频的标题和数量
