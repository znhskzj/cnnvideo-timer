# link_extractor.py v1.2.1

# This script is dedicated to extracting video links from a webpage. It parses the webpage to identify and retrieve URLs of the target videos, preparing them for the subsequent download process.

# link_extractor.py v1.3.0

import requests
import re
import logging
from config_loader import load_config

logger = logging.getLogger('link_extractor')

config = load_config()

class VideoLinkExtractor:
    
    @staticmethod
    def extract_video_links_from_page(url: str = config["YOUTUBE_URL"], max_links: int = config["MAX_VIDEOS_TO_DOWNLOAD"], 
                                      video_pattern: str = config["YOUTUBE_VIDEO_PATTERN"], base_url: str = config["YOUTUBE_BASE_URL"], 
                                      timeout: int = config.get("REQUEST_TIMEOUT", 10)) -> list:
        """
        Extract video links from a webpage.

        Parameters:
        - url: The webpage URL to extract video links from.
        - max_links: Maximum number of video links to return.
        - video_pattern: Regular expression pattern to match video links.
        - base_url: Base URL to construct full video URLs.
        - timeout: Request timeout.

        Returns:
        - A list of video URLs.
        """
        print(f"Timeout value: {timeout}, Type: {type(timeout)}")  # Debug line
        try:
            response = requests.get(url, timeout=timeout)  # Using timeout from config
            response.raise_for_status()  

            video_links = re.findall(video_pattern, response.text)
            full_links = [f'{base_url}/watch?v={link}' for link in video_links]
            return full_links[:max_links]

        except requests.Timeout:
            logger.error(f"Request to {url} timed out.")
        except requests.RequestException as e:
            logger.error(f"Error fetching the page at {url}. Error: {e}")
        
        return []

# Usage example
if __name__ == '__main__':
    links = VideoLinkExtractor.extract_video_links_from_page()
    print(links)
