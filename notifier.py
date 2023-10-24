# notifier.py v1.3.3

# This script is tasked with sending notification emails. It constructs and sends emails to notify users about the availability of new videos or any errors that might have occurred during the video checking or downloading processes.

import smtplib
import logging
import os
import datetime
from email.message import EmailMessage
from config_loader import load_config
from time import sleep
from random import randint

# Set up a logger for this module
logger = logging.getLogger('notifier')

class Notifier:

    def __init__(self):
        """Initialize the Notifier with configuration loaded from the environment file."""
        self.config = load_config()
        self.retry_count = self.config.get("EMAIL_RETRY_COUNT", 3)  # Load retry count from config or use default

        # Assuming SMTP_RECEIVER is a comma-separated string of email addresses.
        self.recipients = [email.strip() for email in self.config["SMTP_RECEIVER"].split(',')]

    def send_notification(self, downloaded_videos):
        """Send an email notification with the titles and sizes of downloaded videos.
        Parameters:
        - downloaded_videos : list : A list of paths to the downloaded videos.
        """

        message_body = ""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Iterating over each downloaded video to create the message body
        for video_path in downloaded_videos:
            video_filename = os.path.basename(video_path)
            video_size = os.path.getsize(video_path)  # Size in bytes
            video_size_mb = video_size / (1024 * 1024)  # Converting size to MB
            message_body += f"Title: {video_filename}, Size: {video_size_mb:.2f} MB\n"  # Adding video info to message body
        
        subject = f"Download Complete: {len(downloaded_videos)} New Videos Downloaded"
        self._send_email(subject, message_body)  # Sending the email notification with video info

    def _send_email(self, subject, body):
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = self.config["SMTP_SENDER"]
        message['To'] = self.recipients
        
        retries = 0
        while retries < self.retry_count:
            try:
                with smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"]) as server:
                    server.starttls()
                    server.login(self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"])
                    server.send_message(message)
                
                logger.info(f"Notification email sent successfully to {', '.join(self.recipients)}!")
                print(f"\nNotification email sent successfully to {', '.join(self.recipients)}!")  # Added print statement
                break  # Exit the loop if the email is sent successfully
                
            except Exception as e:
                logger.error(f"Error sending notification email. Error: {e}. Retrying...")
                retries += 1
                sleep(randint(1, 5))  # Random sleep before retrying

if __name__ == "__main__":
    notifier = Notifier()
    notifier.send_notification(["Test_video.mp4"])  # Test with a dummy video name
