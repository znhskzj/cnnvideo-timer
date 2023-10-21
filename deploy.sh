
#!/bin/bash

# Clone the repository
git clone https://github.com/znhskzj/cnnvideo-timer.git

# Change to the project directory
cd cnnvideo-timer

# Install required packages
pip3 install -r requirements.txt

# Make the scheduler.py executable
chmod +x scheduler.py

# Add the scheduler.py to the crontab for daily execution
(crontab -l 2>/dev/null; echo "0 0 * * * cd $(pwd) && ./scheduler.py") | crontab -
