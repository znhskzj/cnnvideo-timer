# notifier.py v1.3.1

import smtplib
import logging
import os
import datetime
from email.message import EmailMessage
from config_loader import load_config

# Set up a logger for this module
logger = logging.getLogger('notifier')

class Notifier:

    def __init__(self):
        self.config = load_config()
        self.retry_count = 3  # Setting a default retry count of 3 for email failures

        # Assuming SMTP_RECEIVER is a comma-separated string of email addresses.
        self.recipients = [email.strip() for email in self.config["SMTP_RECEIVER"].split(',')]

    def send_notification(self, downloaded_videos):  # Modified to accept a list of downloaded videos
        """Send an email notification with the titles and sizes of downloaded videos."""
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

        with smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"]) as server:
            server.starttls()
            server.login(self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"])
            server.send_message(message)

        logger.info(f"Notification email sent successfully to {', '.join(self.recipients)}!")

if __name__ == "__main__":
    notifier = Notifier()
    notifier.send_notification("Test notification from Notifier.")
