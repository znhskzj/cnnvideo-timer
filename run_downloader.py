import argparse
from download_manager import DownloaderManager, MetadataManager
from video_processor import YTDownloader, VideoLinkExtractor
from config_loader import load_config

def run_downloader():
    config = load_config()

    # create a VideoLinkExtractor instance
    downloader = YTDownloader(output_directory=config["DOWNLOAD_PATH"])
    metadata_manager = MetadataManager(config=config)

    # create a VideoLinkExtractor instance
    extractor = VideoLinkExtractor(config)
    video_links = extractor.extract_video_links_from_page(config["YOUTUBE_URL"])

    # create a list of dictionaries containing video URLs and optional titles
    videos = [{"webpage_url": link, "title":"Default Title"} for link in video_links]  

    # create a DownloaderManager instance，passing config, videos, downloader, and metadata_manager
    downloader_manager = DownloaderManager(videos=videos, downloader=downloader, metadata_manager=metadata_manager, config=config)

    # check and download videos
    downloaded_videos = downloader_manager.check_and_download()

    # print the number of downloaded videos
    print(f"Downloaded videos: {len(downloaded_videos)}")

if __name__ == "__main__":
    run_downloader()
