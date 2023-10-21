# utils.py v1.3.0

# This script provides utility functions, such as sanitizing filenames and setting up logging configurations, that are used across multiple modules in the project.

import os
import re
import logging
from config_loader import load_config

config = load_config()
logger = logging.getLogger('utils')  

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename by replacing special characters."""
    # Replacing forbidden characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]+', '_', filename)  
    filename = re.sub(r'[^a-zA-Z0-9_.-]+', '_', filename)  
    filename = re.sub(r'_+', '_', filename)  
    
    return filename

def setup_logging():
    """Setup the logging system with file and console handlers."""
    log_directory = config.get("LOG_DIRECTORY", "./log")  # Defaulting to ./log if not present
    
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except OSError as e:
            logger.error(f"Error creating log directory: {e}")
            raise

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    log_file_path = os.path.join(log_directory, config.get("LOG_FILENAME", "app.log"))  # Defaulting to app.log if not present
    file_handler = logging.FileHandler(log_file_path)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

def create_directories():
    """Check and create necessary directories."""
    download_path = config.get("DOWNLOAD_PATH", "./videos")  # Defaulting to ./videos if not present
    
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path)
            logger.info(f'Created directory: {download_path}')
        except OSError as e:
            logger.error(f"Error creating videos directory: {e}")
            raise
