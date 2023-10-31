# scheduler.py v1.3.0

# This script is responsible for scheduling and automating the video checking and downloading tasks. It ensures that these tasks are executed at specified intervals, enabling the automatic and timely downloading of new videos.

import os
import argparse
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from utils import sanitize_filename  
from video_downloader import main as video_downloader_main
from notifier import Notifier
from config_loader import load_config

# Setup logger
logger = logging.getLogger('scheduler')
config = load_config()

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Schedule the video downloader job.")
    parser.add_argument('--test', action='store_true', help="Run the job immediately for testing.")
    return parser.parse_args()

def listener(event):
    if event.exception:
        logger.error(f"Scheduler job crashed with exception: {event.exception}")
    else:
        logger.info("Scheduler job completed successfully.")

def job():
    start_time = datetime.now()
    logger.info(f"Starting scheduled video download at {start_time}")
    
    downloaded_titles = video_downloader_main()
    
    if downloaded_titles:
        notifier = Notifier()
        downloaded_video_paths = [os.path.join(config["VIDEO_DIRECTORY"], sanitize_filename(title) + config["VIDEO_EXTENSION"]) 
                                 for title in downloaded_titles]
        notifier.send_notification(downloaded_video_paths)
    
    end_time = datetime.now()
    logger.info(f"Finished downloading {len(downloaded_titles)} videos at {end_time}")

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
    args = parse_arguments()

    if args.test:
        logger.info("Starting test run...")
        job()
        logger.info("Test run completed.")
    else:
        scheduler = BlockingScheduler()
        scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        scheduler.add_job(job, 'interval', hours=12, next_run_time=next_run_time())
        logger.info("Scheduler started...")
        scheduler.start()
