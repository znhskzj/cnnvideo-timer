#!/bin/bash

# File: deploy.sh
# Version: 1.1.0
# Description: This script automates the deployment process of the cnnvideo-timer application. 
# It clones the repository, sets up a virtual environment, installs necessary packages, 
# and schedules the application to run daily.

#!/bin/bash

function clone_repo {
    if [ ! -d "cnnvideo-timer" ]; then
        git clone https://github.com/znhskzj/cnnvideo-timer.git
    else
        echo "Directory cnnvideo-timer already exists. Skipping cloning."
    fi
}

function setup_venv {
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    else
        echo "Virtual environment already exists. Skipping creation."
    fi
}

function install_requirements {
    source venv/bin/activate
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install required packages."
        exit 1
    fi
}

function setup_cron {
    (crontab -l 2>/dev/null; echo "0 0 * * * cd $(pwd) && ./venv/bin/python3 scheduler.py >> cron.log 2>&1") | crontab -
    if [ $? -ne 0 ]; then
        echo "Failed to update crontab."
        exit 1
    fi
}

# Main script execution
clone_repo
cd cnnvideo-timer || exit
setup_venv
install_requirements
setup_cron

echo "Setup completed successfully."
