#  video_downloader.py version 1.7.0

# "This module automatically downloads the latest CNN10 video using yt-dlp, ensuring titles are sanitized and saved to the designated directory."
# -*- coding: utf-8 -*-

# Standard library imports
import os
import logging

# Third-party imports
import yt_dlp.utils
from yt_dlp import YoutubeDL

# Local application imports
from config_loader import load_config
from downloader_checker import DownloaderManager
from utils import setup_logging, create_directories, sanitize_filename
from link_extractor import VideoLinkExtractor
from metadata_manager import MetadataManager  

# 加载配置文件
config = load_config()

# Set up a logger for this module
logger = logging.getLogger('video_downloader')

class YTDownloader:
    def __init__(self, output_directory=None):
        """Initialize the YTDownloader with an output directory.
        Parameters:
        - output_directory : str : The directory where the downloaded videos will be saved.
        """
        if not output_directory:
            output_directory = config["DOWNLOAD_PATH"]
        self.output_directory = output_directory

        yt_dlp.utils.std_headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.ydl_opts = {
            'format': 'best[height<=720][ext=mp4]',
            'outtmpl': os.path.join(self.output_directory, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_progress': True,
            'no_warnings': True,
            'progress_hooks': [self.hook]
        }
        self.ydl = YoutubeDL(self.ydl_opts)

    def hook(self, d):
        """Hook function to handle download progress."""
        if d['status'] == 'downloading':
            print(f"\r[download] {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}", end='')

    def get_video_info(self, video_url):
        """Get video information without downloading the video."""
        return self.ydl.extract_info(video_url, download=False)

    def download_video(self, video_url):
        """Download the video and save it to the specified directory.
        
        Parameters:
        - video_url : str : The URL of the video to be downloaded.
        
        Returns:
        -  
        
        """
        info = self.ydl.extract_info(video_url, download=False)
        clean_title = sanitize_filename(info['title'])
        self.ydl_opts['outtmpl'] = os.path.join(self.output_directory, clean_title + '.%(ext)s')
        self.ydl = YoutubeDL(self.ydl_opts)  # 重新初始化YoutubeDL，使其使用更新的选项
        self.ydl.download([video_url])
        # logger.info(f"Finished downloading video: {video_url}")
        logger.info(f"Successfully downloaded {clean_title}.")

def display_metadata(last_downloaded_titles, config):
    """Display metadata of the downloaded videos."""
    mm = MetadataManager(config)
    videos_metadata = mm.get_all_metadata()
    for metadata in videos_metadata:
        if metadata.get('title') in last_downloaded_titles:
            print(f"Title: {metadata.get('title', 'N/A')}")
            print(f"Uploader: {metadata.get('uploader', 'N/A')}")
            print(f"Published At: {metadata.get('published_at', 'N/A')}")
            print(f"Upload Date: {metadata.get('upload_date', 'N/A')}")
            print(f"Duration: {metadata.get('duration', 'N/A')}")
            print(f"View Count: {metadata.get('view_count', 'N/A')}")
            print(f"Description: {metadata.get('description', 'N/A')}")
            print("-"*50, "\n")

def main():
    """Main function to orchestrate the video downloading."""
    setup_logging()
    create_directories()

    url = config["YOUTUBE_URL"]
    logger.info(f"Extracting video links from: {url}")
    videos = VideoLinkExtractor.extract_video_links_from_page(
        url, 
        max_links=config["MAX_VIDEOS_TO_DOWNLOAD"],
        video_pattern=config["YOUTUBE_VIDEO_PATTERN"],
        base_url=config["YOUTUBE_BASE_URL"]
    )
    logger.info(f"Extracted {len(videos)} video links.")

    downloader = YTDownloader(config["DOWNLOAD_PATH"])
    checker = DownloaderManager(videos, downloader,config)
    logger.info("Starting the checking and downloading process.")
    downloaded_titles, downloaded_count = checker.check_and_download()  # Modified to return downloaded titles

    if downloaded_titles:  # Only if there are new downloaded videos
        message = config["DOWNLOAD_COMPLETE_MESSAGE"].format(len(downloaded_titles))
        print(message)
        logger.info(message)
        
        # Check if user wants to view the metadata
        choice = input(config["VIEW_METADATA_PROMPT"]).strip().lower()  # Sanitize user input
        valid_responses = ['yes', 'y', 'no', 'n']  # Define valid responses
        while choice not in valid_responses:  # Keep asking until a valid response is given
            print("Invalid response. Please enter 'y' or 'n'.")
            choice = input(config["VIEW_METADATA_PROMPT"]).strip().lower()

        if choice in ['yes', 'y']:  # Check against valid affirmative responses
            display_metadata(downloaded_titles, config)
    else:
        message = config["ALL_VIDEOS_DOWNLOADED_MESSAGE"].format(len(downloaded_titles))
        print(message)
        logger.info(message)

    logger.info("Script finished.")
    return downloaded_titles  # Modified to return downloaded titles

if __name__ == "__main__":
    main()
