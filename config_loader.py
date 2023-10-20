# config_loader.py v1.2.2

import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(filename=os.getenv('LOG_FILENAME', 'application.log'), 
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(file_path="config.env"):
    load_dotenv(file_path)

    def get_int_config(key, default_value):
        try:
            return int(os.getenv(key, default_value))
        except ValueError:
            logging.error(f"{key} value in config is not a valid integer. Using default value: {default_value}.")
            return default_value

    config = {
        "YOUTUBE_URL": os.getenv("YOUTUBE_URL", ""),
        "DOWNLOAD_PATH": os.getenv("DOWNLOAD_PATH", "./downloads"),
        "MAX_VIDEOS_TO_DOWNLOAD": get_int_config("MAX_VIDEOS_TO_DOWNLOAD", 1),
        "MAX_DOWNLOAD_RETRIES": get_int_config("MAX_DOWNLOAD_RETRIES", 3),
        "YOUTUBE_VIDEO_PATTERN": os.getenv("YOUTUBE_VIDEO_PATTERN", ""),
        "YOUTUBE_BASE_URL": os.getenv("YOUTUBE_BASE_URL", "https://www.youtube.com"),
        "SMTP_SERVER": os.getenv("SMTP_SERVER", ""),
        "SMTP_PORT": get_int_config("SMTP_PORT", 587),
        "SMTP_USERNAME": os.getenv("SMTP_USERNAME", ""),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
        "SMTP_SENDER": os.getenv("SMTP_SENDER", ""),
        "SMTP_RECEIVER": os.getenv("SMTP_RECEIVER", ""),
        "MORNING_RUN_HOUR": get_int_config("MORNING_RUN_HOUR", 9),
        "MORNING_RUN_MINUTE": get_int_config("MORNING_RUN_MINUTE", 0),
        "EVENING_RUN_HOUR": get_int_config("EVENING_RUN_HOUR", 21),
        "EVENING_RUN_MINUTE": get_int_config("EVENING_RUN_MINUTE", 0),
        "LOG_FILENAME": os.getenv("LOG_FILENAME", "application.log")
    }
    
    return config

if __name__ == "__main__":
    config_data = load_config()
    print(config_data)
