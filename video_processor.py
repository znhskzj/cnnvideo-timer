"""
video_processor.py version 0.9.2 20240212
Merges functionality from link_extractor.py and video_downloader.py into a single module.
This module extracts video links from a specified webpage and downloads the videos.
"""

# Standard library imports
import os
import re
import logging
import requests

# Third-party imports
from yt_dlp import YoutubeDL

# Local application imports
from utils import sanitize_filename

# Set up a logger for this module
logger = logging.getLogger('video_processor')

class YTDownloader:
    """Class for downloading videos using yt-dlp."""

    def __init__(self, output_directory, video_format='18', download_quiet=True):
        """
        Initialize the YTDownloader with the output directory and video format.

        Args:
            output_directory (str): Directory where the videos will be saved.
            video_format (str, optional): Video format code. Defaults to '18'.
            download_quiet (bool, optional): Whether to suppress download output. Defaults to True.
        """
        self.output_directory = output_directory
        self.video_format = video_format
        self.download_quiet = download_quiet
        self.setup_youtube_downloader()

    def setup_youtube_downloader(self):
        """Setup yt-dlp downloader with necessary options."""
        self.ydl_opts = {
            'format': self.video_format,
            'quiet': self.download_quiet,
            'progress_hooks': [self.download_hook],
            'outtmpl': os.path.join(self.output_directory, '%(title)s.%(ext)s')
        }


    def download_hook(self, d):
        """
        Hook function to handle download progress.

        Args:
            d (dict): Dictionary containing information about the download process.
        """
        if d['status'] == 'downloading':
            percent_str = re.sub(r'[^\d.]+', '', d['_percent_str'])  # 使用正则表达式移除非数字字符
            percent = float(percent_str) if percent_str else 0.0
            if percent % 10 == 0:
                print(f"\rDownloading: {percent}% of {d['_total_bytes_str']} at {d['_speed_str']}", end='')
        elif d['status'] == 'finished':
            print("\nDownload finished.")

    def download_video(self, video_info):
        """
        Download the video if it hasn't been downloaded yet.

        Args:
            video_info (dict): Metadata of the video including 'title' and 'webpage_url'.

        Returns:
            bool: True if the video was downloaded, False if the file already existed.
        """
        clean_title = sanitize_filename(video_info['title'])
        output_filepath = os.path.join(self.output_directory, f"{clean_title}.mp4")

        if os.path.exists(output_filepath):
            logger.info(f"File '{clean_title}.mp4' already exists. Skipping download.")
            print(f"File '{clean_title}.mp4' already exists. Skipping download.")  # 直接提示文件已存在，无需下载
            return False  # 返回 False 表示文件已存在，未执行下载
        else:
            with YoutubeDL(self.ydl_opts) as ydl:
                # 在开始下载之前打印一条信息
                print(f"Downloading '{clean_title}.mp4'...")
                ydl.download([video_info['webpage_url']])
                logger.info(f"'{clean_title}.mp4' downloaded.")
                print(f"'{clean_title}.mp4' downloaded.")  # 下载完成后打印信息
            return True  # 返回 True 表示文件已下载

    def get_video_info(self, video_url: str):
        """
        Extract video information without downloading the video.

        Args:
            video_url (str): URL of the video to extract information from.

        Returns:
            dict: Dictionary containing information about the video, or empty dict if extraction fails.
        """
        print(f"Attempting to retrieve video info for URL: {video_url}")
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                # print(f"Video ID: {video_info.get('id', 'N/A')}")
                # print(f"Title: {video_info.get('title', 'N/A')}")
                # print(f"URL: {video_info.get('webpage_url', 'N/A')}")
                return video_info
        except Exception as e:
            logger.error(f"Failed to extract video information for URL {video_url}: {e}")
            return {}

class VideoLinkExtractor:
    """Class for extracting video links from a webpage."""
    def __init__(self, config):
        self.config = config

    def extract_video_links_from_page(self, url, max_links=None):
        """
        Extract video links from the specified webpage.

        Args:
            url (str): The URL of the webpage to extract video links from.
            max_links (int, optional): Maximum number of links to extract.

        Returns:
            list: A list of extracted video links.
        """
        video_pattern = self.config["YOUTUBE_VIDEO_PATTERN"]
        base_url = self.config["YOUTUBE_BASE_URL"]
        timeout = self.config.get("REQUEST_TIMEOUT", 10)

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises HTTPError for bad responses

            video_links = re.findall(video_pattern, response.text)
            full_links = [f"{base_url}/watch?v={link}" for link in video_links]

            # Limit the number of links if max_links is provided
            if max_links is not None:
                full_links = full_links[:max_links]

            return full_links
        except requests.RequestException as e:
            logger.error(f"Error fetching the page at {url}: {e}")
            return []
