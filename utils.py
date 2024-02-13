"""
utils.py v1.4.1

This module provides utility functions such as sanitizing filenames and setting up logging configurations.
These functions are used across multiple modules in the project.
"""

import os
import re
import logging
from typing import NoReturn
from config_loader import load_config

config = load_config()
# Setting up a logger for this module
logger = logging.getLogger(__name__) 

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename by replacing special characters.

    Args:
    - filename (str): The original filename.
    
    Returns:
    - str: A sanitized filename with special characters replaced.
    """
    filename = re.sub(r'[<>:"/\\|?*]+', '_', filename)
    filename = re.sub(r'[^a-zA-Z0-9_.-]+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    return filename

def setup_logging() -> NoReturn:
    """Setup the logging system with file and console handlers.

    Args:
    - None
    
    Returns:
    - NoReturn: This function does not return anything.
    """
    log_directory = config.get("LOG_DIRECTORY", "./log")
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except OSError as e:
            logging.error(f"Error creating log directory: {e}")
            raise

    log_file_path = os.path.join(log_directory, config.get("LOG_FILENAME", "app.log"))
    
    # get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set root logger level
    
    # Remove all pre-existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set up logging for files
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Set up logging for console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Set the log level for 'urllib3' to WARNING to reduce noise in the log file
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def create_directories(directory_path: str) -> NoReturn:
    """Check and create the specified directory if it does not exist.20240212

    Args:
    - directory_path (str): The path of the directory to create.

    Returns:
    - NoReturn: This function does not return anything.
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logger.info(f'Created directory: {directory_path}')
        except OSError as e:
            logger.error(f"Error creating directory at {directory_path}: {e}")
            raise