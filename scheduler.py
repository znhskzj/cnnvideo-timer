# scheduler.py v1.0.4
import os

# Version 1.0.3:
# - Added logger object for the 'scheduler' module.
# - Integrated scheduling times from the configuration file.
# - Added a listener to the BlockingScheduler for better logging.
# Version 1.0.2:
# - Fixed imports and scheduling time for the 9:00 AM and 9:00 PM runs.
# Version 1.0.1:
# - Added a --test flag for immediate execution for testing purposes.
# Version 1.0.0:
# - Initial release with the scheduler to automate the video download and notification process.

import argparse
from utils import sanitize_filename  # Imported sanitize_filename function
from utils import sanitize_filename  # Imported sanitize_filename function
from datetime import datetime, timedelta
from time import sleep
import logging
from video_downloader import main as video_downloader_main
from notifier import Notifier
from config_loader import load_config
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# Setup logger
logger = logging.getLogger('scheduler')

config = load_config()

def job():
    logger.info("Starting scheduled video download...")
    downloaded_titles = video_downloader_main()  # Modified to receive downloaded titles
    
    if downloaded_titles:  # Only if there are new downloaded videos
        notifier = Notifier()
        downloaded_video_paths = []  # List to store the full paths of downloaded videos
        for video_title in downloaded_titles:  # Modified to iterate over downloaded titles
            video_filename = sanitize_filename(video_title)  # Sanitizing the video title
            video_directory = "videos"  # Assuming videos are saved in a "videos" directory
            video_extension = ".mp4"  # Assuming videos are saved with a .mp4 extension
            video_full_path = os.path.join(video_directory, video_filename + video_extension)
            downloaded_video_paths.append(video_full_path)  # Adding the full path to the list
        
        notifier.send_notification(downloaded_video_paths)  # Passing the list of full paths
        logger.info(f"Finished downloading {len(downloaded_titles)} videos.")
        
def listener(event):
    if event.exception:
        logger.error(f"Scheduler job crashed with exception: {event.exception}")
    else:
        logger.info("Scheduler job completed successfully.")

def next_run_time():
    now = datetime.now()
    morning_run = now.replace(hour=config["MORNING_RUN_HOUR"], minute=config["MORNING_RUN_MINUTE"], second=0)
    evening_run = now.replace(hour=config["EVENING_RUN_HOUR"], minute=config["EVENING_RUN_MINUTE"], second=0)
    
    if now < morning_run:
        return morning_run
    elif now < evening_run:
        return evening_run
    else:
        return morning_run + timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule the video downloader job.")
    parser.add_argument('--test', action='store_true', help="Run the job immediately for testing.")
    args = parser.parse_args()

    if args.test:
        logger.info("Starting test run...")
        job()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        scheduler.add_job(job, 'interval', hours=12, next_run_time=next_run_time())
        print("Scheduler started...")
        scheduler.start()
