"""
run_downloader.py version 0.9.2
This module provides the main interface for the video downloading application.
It parses command-line arguments and triggers the appropriate functionality
based on the provided arguments, such as downloading videos or scheduling tasks.
"""

import argparse
from download_manager import DownloaderManager, MetadataManager
from video_processor import YTDownloader, VideoLinkExtractor
from config import ApplicationConfig
from task_scheduler import TaskScheduler, Notifier
from utils import setup_logging
import logging


def run_downloader(video_format, max_videos, video_url, config: ApplicationConfig):
    """
    Executes the video downloading process.

    Args:
        video_format (str): The format code for the videos to be downloaded.
        max_videos (int): The maximum number of videos to download.
        video_url (str): The URL of the webpage where the videos are located.
        config (ApplicationConfig): An instance of ApplicationConfig for accessing configuration settings.
    """
    logger = logging.getLogger(__name__)
    # Initialize downloader, metadata manager, and video link extractor with the ApplicationConfig instance
    downloader = YTDownloader(
        output_directory=config.get("DOWNLOAD_PATH"), video_format=video_format
    )
    metadata_manager = MetadataManager(config=config)
    extractor = VideoLinkExtractor(config)

    logger.info(f"Downloading videos from {video_url}...")
    # Extract video links and prepare video information, then manage downloading and metadata
    video_links = extractor.extract_video_links_from_page(
        video_url, max_links=max_videos
    )
    videos = [{"webpage_url": link, "title": "Default Title"} for link in video_links]
    downloader_manager = DownloaderManager(
        videos=videos,
        downloader=downloader,
        metadata_manager=metadata_manager,
        config=config,
    )
    downloaded_videos = downloader_manager.check_and_download()

    if not downloaded_videos:
        logger.info(
            "No new videos were downloaded. All videos might already exist."
        )  # 使用logger记录
    else:
        logger.info(f"Downloaded {len(downloaded_videos)} video(s).")


def main():
    """
    The main entry point of the application. Parses command-line arguments and triggers the appropriate actions.
    """
    # Setup application-wide logging
    config = ApplicationConfig()  # Load configuration
    setup_logging(config)  # Initialize logging

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Video Downloader and Notifier")
    parser.add_argument(
        "--video_format",
        type=str,
        default="18",
        help="Video format code for downloading.",
    )
    parser.add_argument(
        "--max_videos",
        type=int,
        default=1,
        help="Maximum number of videos to download.",
    )
    parser.add_argument(
        "--video_url",
        type=str,
        help="URL of the video page to download videos from.",
        default=None,
    )
    parser.add_argument(
        "--test", action="store_true", help="Run the job immediately for testing."
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Schedule the video downloading and notification tasks.",
    )
    args = parser.parse_args()

    # Use provided video URL or default to configuration
    video_url = args.video_url if args.video_url else config.get("YOUTUBE_URL")

    # Handle command-line arguments to trigger the appropriate functionality
    if args.test:
        run_downloader(args.video_format, args.max_videos, video_url, config)
    elif args.schedule:
        notifier = Notifier(config)
        task_scheduler = TaskScheduler(config, notifier)
        task_scheduler.schedule_jobs()
        print("Task scheduler started...")
    else:
        print("No arguments provided. Please use --help to see available options.")


if __name__ == "__main__":
    main()
