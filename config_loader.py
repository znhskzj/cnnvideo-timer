# config_loader.py v1.3.1

# This script is responsible for loading and providing configuration values from a specified environment file, ensuring that the application runs with the correct settings.

import os
import logging
import sys  # Importing sys to use sys.exit()
from dotenv import load_dotenv
from typing import Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(file_path: str = "config.env") -> dict[str, Any]:
    """
    Load configuration values from an environment file.
    
    Parameters:
    - file_path : str : Path to the environment file (default is "config.env").
    
    Returns:
    - dict[str, Any] : A dictionary containing the configuration values.
    
    Raises:
    - ValueError : If a configuration value does not match the expected type.
    """
    load_dotenv(file_path)

    # Predefined configuration parameters with their expected types
    config_params = {
        "YOUTUBE_URL": (str, "https://www.youtube.com/@CNN10/videos"),
        "DOWNLOAD_PATH": (str,"./videos"),
        "MAX_VIDEOS_TO_DOWNLOAD": (int, 1),
        "MAX_DOWNLOAD_RETRIES": (int, 3),
        "YOUTUBE_VIDEO_PATTERN": (str,"/watch\?v=([a-zA-Z0-9_-]+)"),
        "YOUTUBE_BASE_URL": (str,"https://www.youtube.com"),
        "SMTP_SERVER": (str,"smtp.gmail.com"),
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
        "LOG_DIRECTORY": (str,"./log"),
        "VIDEO_DIRECTORY": (str, "./videos"),
        "VIDEO_EXTENSION": (str, ".mp4"),
        "DOWNLOAD_COMPLETE_MESSAGE": (str, "All downloads completed. {} videos downloaded."),
        "VIEW_METADATA_PROMPT": (str,"Would you like to view the metadata for downloaded videos? (y/n):"),
        "AFFIRMATIVE_RESPONSE": (str, "y"),
        "ALL_VIDEOS_DOWNLOADED_MESSAGE": (str,"All videos already downloaded. {} videos checked."),
        "REQUEST_TIMEOUT": (int, 10),
        "METADATA_FILE": (str, "./metadata/metadata.json"),
        # ... (add other parameters as needed) ...
    }

    config = {}
    for key, expected_type_default in config_params.items():
        value = os.getenv(key)
        
        # Unpacking the tuple if a default value is provided
        if isinstance(expected_type_default, tuple):
            expected_type, default_value = expected_type_default
            if value is None:
                value = default_value  # Using the default value if the environment variable is missing
        else:
            expected_type = expected_type_default  # No default value provided
        
        # Converting the value to the expected type, if necessary
        if expected_type is int:
            try:
                value = int(value)
            except ValueError:
                error_message = f"{key} value in config is not a valid integer."
                logger.error(error_message)
                raise ValueError(error_message)
        
        config[key] = value
    
    return config

# Example usage
if __name__ == "__main__":
    try:
        config_data = load_config()
        print(config_data)
    except ValueError as e:
        print(f"An error occurred: {e}")