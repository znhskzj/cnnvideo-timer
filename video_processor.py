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
            logger.info(f"[downloading] {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}")
        elif d['status'] == 'finished':
            logger.info("Download finished.")

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
            logger.info(f"'{clean_title}' exists. Skipping download.")
            return False
        else:
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([video_info['webpage_url']])
                logger.info(f"'{clean_title}' downloaded.")
            return True

    def get_video_info(self, video_url: str):
        """
        Extract video information without downloading the video.

        Args:
            video_url (str): URL of the video to extract information from.

        Returns:
            dict: Dictionary containing information about the video, or empty dict if extraction fails.
        """
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                return video_info
        except Exception as e:
            logger.error(f"Failed to extract video information for URL {video_url}: {e}")
            return {}

class VideoLinkExtractor:
    """Class for extracting video links from a webpage."""
    def __init__(self, config):
        # Store the config settings
        self.config = config

    def extract_video_links_from_page(self, url, timeout=10):
        """
        Extract video links from the specified webpage.

        Args:
            url (str): The URL of the webpage to extract video links from.
            max_links (int, optional): Maximum number of links to extract. Defaults to 10.
            video_pattern (str, optional): Regex pattern to match video links. If not provided, defaults to config setting.
            base_url (str, optional): Base URL to prepend to relative video links. If not provided, defaults to config setting.
            timeout (int, optional): Timeout for the HTTP request in seconds. Defaults to 10.

        Returns:
            list: A list of extracted video links.
        """
        # Extract settings from the config
        max_links = self.config["MAX_VIDEOS_TO_DOWNLOAD"]
        video_pattern = self.config["YOUTUBE_VIDEO_PATTERN"]
        base_url = self.config["YOUTUBE_BASE_URL"]
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # 对于错误响应抛出 HTTPError

            video_links = re.findall(video_pattern, response.text)
            full_links = [f"{base_url}/watch?v={link}" for link in video_links][:max_links]

            return full_links
        except requests.RequestException as e:
            logger.error(f"Error fetching the page at {url}: {e}")
            return []