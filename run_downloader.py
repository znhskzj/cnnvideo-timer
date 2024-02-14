"""
run_downloader.py version 0.9.2
This module provides the main interface for the video downloading application.
It parses command-line arguments and triggers the appropriate functionality
based on the provided arguments, such as downloading videos or scheduling tasks.
"""

import argparse
from download_manager import DownloaderManager, MetadataManager
from video_processor import YTDownloader, VideoLinkExtractor
from config_loader import load_config
from task_scheduler import TaskScheduler, Notifier
from utils import setup_logging

def run_downloader(video_format, max_videos, video_url):
    """
    Executes the video downloading process.
    
    Args:
        video_format: The format code for the videos to be downloaded.
        max_videos: The maximum number of videos to download.
        video_url: The URL of the webpage where the videos are located.
    """
    # Load configuration settings
    config = load_config()

    # Initialize downloader, metadata manager, and video link extractor
    downloader = YTDownloader(output_directory=config["DOWNLOAD_PATH"], video_format=video_format)
    metadata_manager = MetadataManager(config=config)
    extractor = VideoLinkExtractor(config)

    # Extract video links and prepare video information
    video_links = extractor.extract_video_links_from_page(video_url, max_links=max_videos)
    videos = [{"webpage_url": link, "title": "Default Title"} for link in video_links]

    # Manage video downloading and metadata storing
    downloader_manager = DownloaderManager(videos=videos, downloader=downloader, metadata_manager=metadata_manager, config=config)
    downloaded_videos = downloader_manager.check_and_download()

    # Print the number of successfully downloaded videos
    print(f"Downloaded videos: {len(downloaded_videos)}")

def main():
    """
    The main entry point of the application. Parses command-line arguments and triggers the appropriate actions.
    """
    # Setup application-wide logging
    setup_logging()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Video Downloader and Notifier")
    parser.add_argument('--video_format', type=str, default='18', help="Video format code for downloading.")
    parser.add_argument('--max_videos', type=int, default=1, help="Maximum number of videos to download.")
    parser.add_argument('--video_url', type=str, help="URL of the video page to download videos from.", default=None)
    parser.add_argument('--test', action='store_true', help="Run the job immediately for testing.")
    parser.add_argument('--schedule', action='store_true', help="Schedule the video downloading and notification tasks.")
    args = parser.parse_args()

    # Use provided video URL or default to configuration
    video_url = args.video_url if args.video_url else load_config()["YOUTUBE_URL"]

    # Handle command-line arguments to trigger the appropriate functionality
    if args.test:
        run_downloader(args.video_format, args.max_videos, video_url)
    elif args.schedule:
        config = load_config()
        notifier = Notifier(config)
        task_scheduler = TaskScheduler(config, notifier)
        task_scheduler.schedule_jobs()
        print("Task scheduler started...")
    else:
        print("No arguments provided. Please use --help to see available options.")

if __name__ == "__main__":
    main()
