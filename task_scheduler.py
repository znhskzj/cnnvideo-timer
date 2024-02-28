"""
task_scheduler.py version 0.9.2
Combines functionalities of notifier and scheduler into a unified module.
This module is responsible for sending notification emails about newly downloaded videos and
scheduling video download tasks at specified intervals.
"""

import os
import argparse
import time
from random import randint
from typing import List
from config import ApplicationConfig

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

import smtplib
import logging
from email.message import EmailMessage
from datetime import datetime

# Initialize logger for this module
logger = logging.getLogger("task_scheduler")


class Notifier:
    def __init__(self, config: ApplicationConfig):
        """Initializes Notifier with configuration settings."""
        self.config = config
        self.retry_count = self.config.get("EMAIL_RETRY_COUNT", 3)
        self.recipients = [
            email.strip() for email in self.config。get("SMTP_RECEIVER","").split(",")
        ]

    def send_notification(self, downloaded_videos: List[str]):
        """Sends an email notification about the downloaded videos."""
        message_body = "The following videos have been downloaded:\n\n"
        current_date = datetime.now().strftime("%Y-%m-%d")

        for video_path in downloaded_videos:
            video_filename = os.path.basename(video_path)
            video_size = os.path.getsize(video_path)
            video_size_mb = video_size / (1024 * 1024)
            message_body += f"- {video_filename}, Size: {video_size_mb:.2f} MB\n"

        subject = f"New Videos Downloaded on {current_date}"
        self._send_email(subject, message_body)

    def _send_email(self, subject: str, body: str):
        """Private method to send an email with the given subject and body."""
        message = EmailMessage()
        message.set_content(body)
        message["Subject"] = subject
        message["From"] = self.config["SMTP_SENDER"]
        message["To"] = ", ".join(self.recipients)

        retries = 0
        while retries < self.retry_count:
            try:
                with smtplib.SMTP(
                    self.config["SMTP_SERVER"], self.config["SMTP_PORT"]
                ) as server:
                    server.starttls()
                    server.login(
                        self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"]
                    )
                    server.send_message(message)

                logger.info(f"Notification email sent successfully.")
                break
            except smtplib.SMTPException as e:
                logger.error(f"Error sending email: {e}. Retrying...")
                retries += 1
                time.sleep(randint(1, 5))


class TaskScheduler:
    def __init__(self, config: ApplicationConfig, notifier: Notifier):
        """Initializes TaskScheduler with configuration settings and Notifier instance."""
        self.config = config
        self.notifier = notifier
        self.scheduler = BlockingScheduler()

    def listener(self, event):
        """Handles scheduler job events."""
        if event.exception:
            logger.error("Scheduler job crashed")
        else:
            logger.info("Scheduler job completed")

    def schedule_jobs(self):
        """Schedules video download tasks."""
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        # Define and schedule your video download tasks here
        logger.info("Scheduler started.")
        self.scheduler.start()


def main():
    """Main function to parse arguments and start the task scheduler."""
    config = ApplicationConfig()
    notifier = Notifier(config)
    task_scheduler = TaskScheduler(config, notifier)

    parser = argparse.ArgumentParser(
        description="Task Scheduler for Video Downloading and Notifications"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run the job immediately for testing."
    )
    args = parser.parse_args()

    if args.test:
        logger.info("Starting test run...")
        # Define test job execution logic here
        pass
    else:
        task_scheduler.schedule_jobs()


if __name__ == "__main__":
    main()
