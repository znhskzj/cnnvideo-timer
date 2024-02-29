"""
download_manager.py version 0.9.2 20240213
To manage the downloading process of videos from various sources. 
It integrates functionalities for checking video existence, downloading videos, and managing video metadata into a cohesive system. 
Utilizing the YTDownloader for video downloads and MetadataManager for metadata handling, it ensures that videos are efficiently 
downloaded and stored with relevant metadata, avoiding unnecessary re-downloads and organizing video data for easy access and reference.

Merges the functionality of youtube_metadata_checker.py and downloader_checker.py and metadata_manager.py into a single class DownloaderManager.20240212

"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from utils import sanitize_filename
from config import ApplicationConfig

logger = logging.getLogger(__name__)


class DownloaderManager:
    def __init__(
        self,
        videos: List[Dict[str, str]],
        downloader: Any,
        metadata_manager: "MetadataManager",
        config: ApplicationConfig,
    ) -> None:
        """Initialize the DownloaderManager with videos to be downloaded, a downloader, and configuration.

        Args:
            videos (List[Dict[str, str]]): A list of video information to be downloaded.
            downloader (YTDownloader): An instance of YTDownloader to perform the actual download.
            metadata_manager (MetadataManager): An instance of MetadataManager to handle metadata.
            config (ApplicationConfig): An instance of the ApplicationConfig class, used to retrieve configuration settings.

        Returns:
        - None
        """
        self.videos = videos
        self.downloader = downloader
        self.metadata_manager = metadata_manager
        self.config = config

    def should_download(self, video_info: Dict[str, str]) -> bool:
        """Determine if a video should be downloaded based on its title and metadata.

        Args:
        - video_info : dict : Information about the video to be downloaded.

        Returns:
        - bool : True if the video should be downloaded, False otherwise.
        """
        sanitized_title = sanitize_filename(video_info["title"])
        video_path = os.path.join(
            self.downloader.output_directory,
            sanitized_title + self.config.get("VIDEO_EXTENSION", ".mp4"),
        )
        return not os.path.exists(video_path)

    def store_video_metadata(self, video_info: Dict[str, str]) -> None:
        """Store video metadata using MetadataManager.

        Parameters:
        - video_info : dict : Information about the video to be downloaded.

        Returns:
        - None
        """
        video_title = video_info.get(
            "title", "Default Title"
        )  # from video_info, get the title, or use 'Default Title' if not found
        sanitized_title = sanitize_filename(
            video_title
        )  # use the sanitize_filename function to clean up the title
        video_path = os.path.join(
            self.downloader.output_directory, f"{sanitized_title}.mp4"
        )  # use the sanitized title to create the video path

        metadata = {
            "id": video_info["id"],
            "title": video_title,
            "url": video_info["webpage_url"],
            "description": video_info.get("description", ""),
            "published_at": video_info.get("upload_date", "Unknown Date"),
            "video_path": video_path,
            "downloaded_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.metadata_manager.save_or_update_metadata(metadata)

    def check_and_download(self) -> List[str]:
        downloaded_filenames = []
        for video in self.videos:
            video_url = video["webpage_url"]
            video_info = self.downloader.get_video_info(video_url)
            if video_info and self.should_download(video_info):
                logger.info(f"Attempting to download: {video_info['title']}")
                if self.downloader.download_video(video_info):
                    self.store_video_metadata(video_info)
                    downloaded_filename = sanitize_filename(
                        video_info["title"]
                    ) + self.config.get("VIDEO_EXTENSION", ".mp4")
                    downloaded_filenames.append(downloaded_filename)
                    logger.info(f"'{downloaded_filename}' downloaded successfully.")
                else:
                    logger.info(
                        f"Skipping download for '{video_info['title']}' - file already exists."
                    )
            else:
                logger.info(
                    f"Skipping download for '{video_info['title']}' - not required or already exists."
                )
        return downloaded_filenames


class MetadataManager:
    def __init__(self, config: ApplicationConfig):
        """
        Initialize the MetadataManager with a configuration instance.

        Args:
            config (ApplicationConfig): The ApplicationConfig instance containing settings and parameters.

        Returns:
        - None
        """
        self.metadata_file_path = config.get("METADATA_FILE", "metadata.json")

    def save_or_update_metadata(self, metadata: Dict[str, Any]):
        """Save or update the metadata of a video.

        Args:
        - metadata (Dict): The metadata dictionary to be saved or updated.

        Returns:
        - None
        """
        all_metadata = self.get_all_metadata()
        all_metadata[metadata["id"]] = metadata
        self._save_metadata(all_metadata)

    def get_all_metadata(self) -> Dict[str, Any]:
        """Retrieve all stored metadata.

        Returns:
        - Dict: A dictionary containing all stored metadata.
        """
        try:
            with open(self.metadata_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def query_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Query metadata of a specific video using its video ID.

        Args:
        - video_id (str): The video ID used to query its metadata.

        Returns:
        - Optional[Dict]: The metadata of the specified video, or None if not found.
        """
        return self.get_all_metadata().get(video_id)

    def _save_metadata(self, all_metadata: Dict[str, Any]):
        """Save all metadata to the metadata file.

        Args:
        - all_metadata (Dict[str, Any]): All metadata to be saved.

        Returns:
        - None
        """
        os.makedirs(os.path.dirname(self.metadata_file_path), exist_ok=True)
        with open(self.metadata_file_path, "w", encoding="utf-8") as file:
            json.dump(all_metadata, file, ensure_ascii=False, indent=4)
