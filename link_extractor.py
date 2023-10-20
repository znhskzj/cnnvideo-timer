# link_extractor.py v1.1.0

import requests
import re
import logging

logger = logging.getLogger('link_extractor')

class VideoLinkExtractor:
    
    @staticmethod
    def extract_video_links_from_page(url, max_links=None, video_pattern=None, base_url=None):
        if max_links is None or video_pattern is None or base_url is None:
            # 您可以在这里抛出异常，或者使用默认值。这里为了简洁，我选择了抛出异常。
            raise ValueError("Necessary parameters are missing!")
        
        try:
            response = requests.get(url, timeout=10)  # 10秒的超时限制
            response.raise_for_status()  # 这会引发HTTPError，如果返回的是一个不成功的状态码

            video_links = re.findall(video_pattern, response.text)
            full_links = [f'{base_url}/watch?v={link}' for link in video_links]
            return full_links[:max_links]

        except requests.Timeout:
            logger.error(f"Request to {url} timed out.")
        except requests.RequestException as e:
            logger.error(f"Error fetching the page at {url}. Error: {e}")
        
        return []

# 当您实际使用这个方法时，从 config 中获取所需的值：
if __name__ == '__main__':
    from config_loader import load_config

    config = load_config()
    url = "YOUR_URL_HERE"
    links = VideoLinkExtractor.extract_video_links_from_page(
        url, 
        max_links=config["MAX_VIDEOS_TO_DOWNLOAD"],
        video_pattern=config["YOUTUBE_VIDEO_PATTERN"],
        base_url=config["YOUTUBE_BASE_URL"]
    )
    print(links)
