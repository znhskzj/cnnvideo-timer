# CNN Video Timer
CNN Video Timer is a tool designed for scheduling the checking and downloading of videos from CNN, with automated link extraction, video downloading, and timed task execution, complemented by email notifications upon download completion.

## Feature Introduction
CNN Video Timer is a tool for scheduling the checking and downloading of CNN videos. It can automatically extract the links of CNN10 English news YouTube videos, download the videos, and can be configured to execute these tasks at scheduled times. Upon the completion of downloads, it can send notifications via email.

This project is planned for refactoring to implement more features, and a link to the new project will be published shortly.

## File Structure (Sorted alphabetically)
- `.gitignore`: Excludes files including logs, metadata, downloaded videos, local configurations, keys, temporary files, etc.
- `baidu_cloud_uploader.py`: Baidu Cloud upload module, responsible for uploading downloaded videos to Baidu Cloud (Baidu API setup and user access token authorization required)
- `build.bat`: Packaging module for administrators, moves configuration files out of the working directory, uses pyinstaller to create 2 release packages, one containing ffmpeg.exe.
- `CHANGELOG.md`: Version update records for each module
- `config_loader.py`: Configuration loading module, responsible for loading and validating environment configurations
- `configenv`: Reference configuration file, needs to be renamed to config.env and set with the respective parameters
- `deploy.sh`: One-click installation script for Linux Ubuntu, used for automatic project deployment
- `downloader_checker.py`: Download checker module, responsible for checking and managing video downloads
- `install.bat`: Installation script for Windows users, to be executed in a Windows window after downloading the full version, creates a bin directory, and moves ffmege to bin directory, adding to the system path.
- `LICENSE.md`: MIT License
- `link_extractor.py`: Link extraction module, responsible for extracting video links from web pages
- `metadata_manager.py`: Metadata management module, responsible for managing video metadata
- `notifier.py`: Notification module, responsible for sending email notifications upon download completion (user email parameters to be set in configuration file beforehand)
- `README.md`: This documentation
- `requirements.txt`: Project dependencies include apscheduler, python-dotenv, requests, yt_dlp; additionally, ffmpeg.exe needs to be downloaded to bin directory in advance
- `scheduler.py`: Scheduler module, responsible for scheduling download tasks, download times can be set in configuration file, use --test parameter for immediate execution when run independently
- `utils.py`: Utility module, includes log setup, directory check and creation, and filename cleaning
- `video_downloader.py`: Video downloader module, responsible for video downloads
- `bin/`: Houses third-party tools, currently `ffmpeg.exe`, `ffprobe.exe` and `ffplay.exe`
- `log/`: Holds log files, log filename is video_downloader.log
- `metadata/`: Holds metadata information for downloaded videos, metadata filename is metadata.json
- `videos/`: Holds downloaded video files, videos are organized by date

## Update Log
Please refer to the `CHANGELOG.md` file for a detailed update log.

## Dependencies
- Python 3
- FFmpeg, please download ffmpeg.exe and place it in the bin subdirectory of this project, download link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- Other Python libraries: apscheduler, python-dotenv, requests, yt_dlp, for specific version numbers please refer to `requirements.txt` file

## How to Use
### Windows
#### Method One (Recommended)
1. Direct Download: https://github.com/znhskzj/cnnvideo-timer/releases/download/v0.9.1/releaseffmpeg.zip
2. Create a new directory locally, and unzip the file above.
3. Execute the install.bat script (for Windows 10 and above users, if below Windows 10, install unzip software and refer to Method Two below).

#### Method Two
1. In the repository at https://github.com/znhskzj/cnnvideo-timer, on the release page, download the latest version.
2. If you haven't downloaded ffmpeg.exe before, please download releaseffmpeg.zip.
3. Unzip to a separate working directory, create a bin subdirectory, place ffmpeg.exe in the subdirectory, and add the directory to the system environment path.
4. Rename configenv to config.env.
5. Execute cnn10vd.exe file, video files will be downloaded to the video subdirectory of the current directory.

#### Programmers
1. Please go to https://github.com/znhskzj/cnnvideo-timer to download the source code.
2. Rename configenv to config.env and configure the parameters.
3. Various fancy usages include real-time downloading, scheduled downloading, downloading multiple videos, switching to other news channels for downloading, changing download file specifications, viewing YouTube video metadata, uploading to Baidu Cloud Disk, etc.
4. Stars, forks, and PRs are welcomed.

### Mac and Linux
1. Ensure Python is installed.
2. Run the following command for one-click automatic project deployment (Ubuntu and Debian):

curl -sSL https://raw.githubusercontent.com/znhskzj/cnnvideo-timer/main/deploy.sh | bash

For manual deployment, ensure the deploy.sh script has execution permissions. Use the following commands to check and set:
chmod +x deploy.sh

## Common Questions
For installation issues on Linux, please refer to the FAQ.md document.
Contribution
If you have any questions or suggestions, or wish to contribute to the project, you can contact us via email or raise an Issue or Pull Request in the project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Risk Warning
When using this tool and downloading videos, please comply with relevant laws and regulations, as well as the terms and conditions of the video creators, and respect copyrights.

## Contact Information
For any questions or suggestions, please email: admin@zhurong.link
