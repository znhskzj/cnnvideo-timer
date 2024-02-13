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
from config_loader import load_config
from utils import setup_logging, create_directories, sanitize_filename
from metadata_manager import MetadataManager  

# Load configuration file
config = load_config()

# Set up a logger for this module
logger = logging.getLogger('video_processor')

class YTDownloader:
    """A class for downloading videos using yt-dlp.

    Attributes:
        output_directory (str): the directory where the videos will be saved.
        ydl_opts (dict): yt-dlp options for downloading videos.
        ydl (YoutubeDL): yt-dlp instance for downloading videos.
    """

    def __init__(self, output_directory=None):
        """Initialize the YTDownloader with the output directory.

        Args:
            output_directory (str, optional): The directory where the videos will be saved. Defaults to config["DOWNLOAD_PATH"].
        """
        self.output_directory = output_directory or config["DOWNLOAD_PATH"]
        self.setup_youtube_downloader()

    def setup_youtube_downloader(self):
        """Setup the yt-dlp downloader with necessary options.
    
        Args:
            self (YTDownloader): An instance of YTDownloader.

        Returns:
            None
        """
        self.ydl_opts = {
            'format': '18', # Specify the video format code   
            'outtmpl': os.path.join(self.output_directory, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_progress': True,
            'no_warnings': True,
            'progress_hooks': [self.download_hook],
        }
        self.ydl = YoutubeDL(self.ydl_opts)

    def download_hook(self, d):
        """Hook function to handle download progress.

        Args:
        - d(dict) : A dictionary containing information about the download process such as 'status', '_percent_str', '_total_bytes_str', and '_speed_str'.
        
        Returns:
        - None
        """
        if d['status'] == 'downloading':
            print(f"\r[downloading] {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}", end='', flush=True)
        elif d['status'] == 'finished':
            print("downloading finished")  
        
    def download_video(self, video_info):
        """Download the video if it hasn't been downloaded yet, and return whether the download was performed.
        
        Args:
            video_info (dict): The video's metadata, include 'title' and 'webpage_url'.
        
        Returns:
            bool: True if the video was downloaded, False if the file already existed.
        """
        clean_title = sanitize_filename(video_info['title'])
        output_filepath = os.path.join(self.output_directory, f"{clean_title}.mp4")  # Adjust format if necessary

        if os.path.exists(output_filepath):
            # Simplified log message
            logger.info(f"'{clean_title}' exists.")
            return False  # No download performed because file exists
        else:
            self.ydl_opts['outtmpl'] = output_filepath
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([video_info['webpage_url']])
                # Simplified log message for successful download
                logger.info(f"'{clean_title}' downloaded.")
            return True  # Download was performed

    def get_video_info(self, video_url: str) -> dict:
        """Extract video information without downloading the video.

        Args:
            video_url (str): The URL of the video to extract information from.

        Returns:
            dict: A dictionary containing various pieces of information about the video.
        """
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                video_info = ydl.extract_info(video_url, download=False)
                return video_info
        except Exception as e:
            logger.error(f"Failed to extract video information for URL {video_url}: {e}")
            return {}    

class VideoLinkExtractor:
    """A class for extracting video links from a specified webpage."""

    @staticmethod
    def extract_video_links_from_page(url, max_links=10, video_pattern=None, base_url=None, timeout=10):
        """
        Extract video links from a webpage.

        Args:
        - url (str): The URL of the webpage to extract video links from. Defaults to config["YOUTUBE_URL"].
        - max_links (int): The maximum number of links to extract. Defaults to config["MAX_VIDEOS_TO_DOWNLOAD"].
        - video_pattern (str): The regex pattern to match video links. Defaults to config["YOUTUBE_VIDEO_PATTERN"].
        - base_url (str): The base URL to prepend to relative video links. Defaults to config["YOUTUBE_BASE_URL"].
        - timeout (float): The timeout for the HTTP request in seconds. Defaults to config.get("REQUEST_TIMEOUT", 10).

        Returns:
        - list: A list of extracted video links, or an empty list if an error occurs.
        """
        video_pattern = video_pattern or config["YOUTUBE_VIDEO_PATTERN"]
        base_url = base_url or config["YOUTUBE_BASE_URL"]
        response = requests.get(url, timeout=timeout)

        try:
            response.raise_for_status()  
            video_links = re.findall(video_pattern, response.text)
            full_links = [f'{base_url}/watch?v={link}' for link in video_links]
            return full_links[:max_links]
        except requests.RequestException as e:
            logging.error(f"Error fetching the page at {url}. Error:{e}")
            return []

def display_metadata(last_downloaded_titles, config):
    """Display metadata of the downloaded videos.
    
    Args:
    - last_downloaded_titles : list of str : A list of titles of the videos that were downloaded in the last run.
    - config(dict) : A configuration dictionary containing various settings and parameters used throughout the script.
    
    Returns:
    - None
    """
    mm = MetadataManager(config)
    videos_metadata = mm.get_all_metadata()  # This is a dict where keys are video IDs and values are metadata dicts

    # Iterate over the values of the videos_metadata dict, which are the metadata dicts for each video
    for metadata in videos_metadata.values():
        # Now 'metadata' is a dict, so we can safely use .get() on it
        if metadata.get('title') in last_downloaded_titles:
            print(f"Title: {metadata.get('title', 'N/A')}")
            print(f"Uploader: {metadata.get('uploader', 'N/A')}")
            print(f"Published At: {metadata.get('published_at', 'N/A')}")
            print(f"Upload Date: {metadata.get('upload_date', 'N/A')}")
            print(f"Duration: {metadata.get('duration', 'N/A')}")
            print(f"View Count: {metadata.get('view_count', 'N/A')}")
            print(f"Description: {metadata.get('description', 'N/A')}")
            print("-" * 50, "\n")

def main():
    """
    Main function that orchestrates the video downloading process.
    It extracts video links, downloads videos, and uploads them to Baidu Netdisk.
    
    Returns:
    - list : A list containing the filenames of the videos that were successfully downloaded.
    """

    # Check if config.env file exists
    if not os.path.exists('config.env'):
        print("Error: config.env file not found.")
        exit(1)
        
    # Setup logging and directories
    setup_logging()
    create_directories(config["DOWNLOAD_PATH"])
    
    # Extract video URLs
    url = config["YOUTUBE_URL"]
    videos = VideoLinkExtractor.extract_video_links_from_page(url, max_links=config["MAX_VIDEOS_TO_DOWNLOAD"])
    if not videos:
        print("No videos found. Exiting...")
        return
    
    # Initialize downloader and checker
    downloader = YTDownloader(config["DOWNLOAD_PATH"])
    downloaded_titles = []

    download_performed = False  # Track if any download was performed

    for video_url in videos:
        video_info = downloader.get_video_info(video_url)
        if downloader.download_video(video_info):
            download_performed = True  # Set to True if any video was downloaded

    if download_performed:
        print("Videos downloaded successfully.")
    else:
        print("No new videos were downloaded.")

if __name__ == "__main__":
    main()