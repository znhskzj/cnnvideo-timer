# config.py

"""
Configuration Management Module

This module is responsible for loading and managing application configurations such as API keys, download paths, etc.
It utilizes dotenv to load environment variables and provides an ApplicationConfig class to simplify access to configuration items.

"""

import os
from dotenv import load_dotenv


class ApplicationConfig:
    def __init__(self, config_file="config.env"):
        load_dotenv(config_file)
        self.config = self._load_config()

    def _load_config(self):
        config_params = {
            "YOUTUBE_URL": ("https://www.youtube.com/@CNN10/videos", str),
            "DOWNLOAD_PATH": ("./videos", str),
            "VIDEO_EXTENSION": (str, ".mp4"),
            "MAX_VIDEOS_TO_DOWNLOAD": (int, 1),
            "MAX_DOWNLOAD_RETRIES": (int, 3),
            "YOUTUBE_VIDEO_PATTERN": (str, "/watch\?v=([a-zA-Z0-9_-]+)"),
            "YOUTUBE_BASE_URL": (str, "https://www.youtube.com"),
            "SMTP_SERVER": (str, "smtp.gmail.com"),
            "SMTP_PORT": (int, 587),
            "SMTP_USERNAME": str,
            "SMTP_PASSWORD": str,
            "SMTP_SENDER": str,
            "SMTP_RECEIVER": str,
            "MORNING_RUN_HOUR": (int, 9),
            "MORNING_RUN_MINUTE": (int, 0),
            "EVENING_RUN_HOUR": (int, 21),
            "EVENING_RUN_MINUTE": (int, 0),
            "LOG_FILENAME": (str, "video_downloader.log"),
            "LOG_DIRECTORY": (str, "./log"),
            "VIDEO_DIRECTORY": (str, "./videos"),
            "VIDEO_EXTENSION": (str, ".mp4"),
            "DOWNLOAD_COMPLETE_MESSAGE": (
                str,
                "All downloads completed. {} videos downloaded.",
            ),
            "VIEW_METADATA_PROMPT": (
                str,
                "Would you like to view the metadata for downloaded videos? (y/n):",
            ),
            "AFFIRMATIVE_RESPONSE": (str, "y"),
            "ALL_VIDEOS_DOWNLOADED_MESSAGE": (
                str,
                "All videos already downloaded. {} videos checked.",
            ),
            "REQUEST_TIMEOUT": (int, 10),
            "METADATA_FILE": (str, "./metadata/metadata.json"),
            "YOUTUBE_API_KEY": str,
            "BAIDU_APPID": str,
            "BAIDU_APIKEY": str,
            "BAIDU_SECRETKEY": str,
            "BAIDU_SIGNKEY": str,
            "BAIDU_REDIRECT_URI": str,
            "BAIDU_APP_NAME": str,
            "BAIDU_ACCESS_TOKEN": str,
            "DEFAULT_METADATA_EXTRACTOR": (str, "yt_dlp"),
            "METADATA_DIRECTORY": (str, "./metadata"),
            "MAX_RESOLUTION": (int, 720),
        }

        config = {}
        for key, (default, expected_type) in config_params.items():
            value = os.getenv(key, default)
            if expected_type is int:
                try:
                    value = int(value)
                except ValueError:
                    raise ValueError(f"Config error: {key} should be an integer.")
            config[key] = value
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

    # Example properties
    @property
    def youtube_url(self):
        return self.get("YOUTUBE_URL")

    @property
    def download_path(self):
        return self.get("DOWNLOAD_PATH")

    @property
    def max_videos_to_download(self):
        return self.get("MAX_VIDEOS_TO_DOWNLOAD", 1)

    # Add more properties as needed...
