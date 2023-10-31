# link_extractor.py v1.4.1

import requests
import re
import logging
from config_loader import load_config

logger = logging.getLogger('link_extractor')

config = load_config()

class VideoLinkExtractor:
    
    @staticmethod
    def extract_video_links_from_page(url=None, max_links=None, video_pattern=None, base_url=None, timeout=None) -> list:
        """
        Extract video links from a webpage.

        Parameters are loaded from configuration if not provided.
        """
        url = url or config["YOUTUBE_URL"]
        max_links = max_links or config["MAX_VIDEOS_TO_DOWNLOAD"]
        video_pattern = video_pattern or config["YOUTUBE_VIDEO_PATTERN"]
        base_url = base_url or config["YOUTUBE_BASE_URL"]
        timeout = timeout or config.get("REQUEST_TIMEOUT", 10)

        # 确保 max_links 是整数
        if not isinstance(max_links, int):
            try:
                max_links = int(max_links)
            except ValueError:
                logger.error(f"Invalid MAX_VIDEOS_TO_DOWNLOAD value: {max_links}. It must be an integer.")
                return []

        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  

            video_links = re.findall(video_pattern, response.text)
            full_links = [f'{base_url}/watch?v={link}' for link in video_links]
            return full_links[:max_links]

        except requests.Timeout:
            logger.error(f"Request to {url} timed out after {timeout} seconds.")
        except requests.RequestException as e:
            logger.error(f"Error fetching the page at {url}. Error: {e}")
        
        return []

# Usage example
if __name__ == '__main__':
    links = VideoLinkExtractor.extract_video_links_from_page()
    print(links)
