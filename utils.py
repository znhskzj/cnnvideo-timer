"""
utils.py version 0.9.2

This module provides utility functions such as sanitizing filenames and setting up logging configurations.
These functions are used across multiple modules in the project.
"""

import os
import re
import logging
from typing import Optional
from config import ApplicationConfig

# Configure a module-level logger
logger = logging.getLogger(__name__)


def setup_logging(config: ApplicationConfig):
    """
    Configures the logging system to include both file and console logging.

    This function sets up the logging system with two handlers: one for writing logs to a file, and another for outputting logs to the console. The logging level, format, and destinations are configurable through the ApplicationConfig instance.

    Args:
        config (ApplicationConfig): An instance of the application configuration, used to retrieve logging configurations.

    Returns:
        None
    """

    # Retrieve log directory and filename from the configuration, or use defaults if not set
    log_directory = config.get("LOG_DIRECTORY", "./log")
    log_filename = config.get("LOG_FILENAME", "app.log")

    # Ensure the log directory exists, create it if necessary
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Build the full path for the log file
    log_file_path = os.path.join(log_directory, log_filename)

    # Use basicConfig to set up logging format and add file and console handlers in one go
    logging.basicConfig(
        level=config.get(
            "LOG_LEVEL", "INFO"
        ),  # Retrieve log level from config, default to INFO
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.FileHandler(log_file_path),  # File handler for logging to a file
            logging.StreamHandler(),  # Console handler for logging to stdout
        ],
    )


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by replacing special characters.

    Args:
        filename (str): The original filename.

    Returns:
        str: A sanitized filename with special characters replaced.
    """
    filename = re.sub(r'[<>:"/\\|?*]+', "_", filename)
    filename = re.sub(r"[^a-zA-Z0-9_.-]+", "_", filename)
    filename = re.sub(r"_+", "_", filename)
    return filename


def create_directories(directory_path: str) -> None:
    """
    Checks and creates the specified directory if it does not exist.

    Args:
        directory_path (str): The path of the directory to create.

    Returns:
        None
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        except OSError as e:
            logger.error(f"Error creating directory at {directory_path}: {e}")
            raise


def extract_video_id(video_url: str) -> Optional[str]:
    """
    Extracts the video ID from a YouTube video URL.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        Optional[str]: The extracted video ID, or None if extraction fails.
    """
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", video_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        logger.error(f"Failed to extract video ID from URL: {video_url}")
        return None
