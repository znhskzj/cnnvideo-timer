#!/bin/bash

# File: deploy.sh
# Version: 1.2.0
# Description: This script automates the deployment process of the cnnvideo-timer application. 
# It clones the repository, sets up a virtual environment, installs necessary packages, 
# sets the time zone, and schedules the application to run daily.

function check_commands {
    commands=("git" "python3" "pip3")
    for cmd in "${commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            echo "$cmd could not be found, please install it."
            exit 1
        fi
    done
}

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

function set_timezone {
    timedatectl set-timezone America/New_York
}

function setup_cron {
    (crontab -l 2>/dev/null; echo "0 0 * * * cd $(pwd) && ./venv/bin/python3 scheduler.py >> cron.log 2>&1") | crontab -
    if [ $? -ne 0 ]; then
        echo "Failed to update crontab."
        exit 1
    fi
}

# Main script execution
check_commands
clone_repo
cd cnnvideo-timer || exit
setup_venv
install_requirements
set_timezone
setup_cron

echo "Setup completed successfully."
