@echo off
:: build.bat version 1.0.2
:: This script automates the process of packaging the video_downloader application.
:: It performs the following steps:
:: 1. Checks for the existence of config.env, configenv, and install.bat in the working directory.
:: 2. Moves config.env, configenv, and install.bat to a backup directory.
:: 3. Runs PyInstaller to package the application.
:: 4. Creates two zip files for distribution:
::    - release.zip contains the built executable, configenv, and install.bat.
::    - releaseffmpeg.zip contains the built executable, configenv, ffmpeg.exe, and install.bat.
:: 5. Restores config.env, configenv, and install.bat back to the working directory.

setlocal

:: Define the directories
set WORK_DIR=d:\program\cnnvideo-timer
set BACKUP_DIR=d:\program

:: Change to the working directory
cd /d %WORK_DIR%

:: Check if config.env, configenv, and install.bat exist in the working directory
if not exist config.env (
    echo config.env does not exist in the working directory. Aborting.
    exit /b 1
)

if not exist configenv (
    echo configenv does not exist in the working directory. Aborting.
    exit /b 1
)

if not exist install.bat (
    echo install.bat does not exist in the working directory. Aborting.
    exit /b 1
)

@REM if not exist run_videodownload.bat (
@REM     echo run_videodownload does not exist in the working directory. Aborting.
@REM     exit /b 1
@REM )

:: Move config.env, configenv, and install.bat to the backup directory
echo Moving config.env, configenv, and install.bat to the backup directory...
move config.env %BACKUP_DIR%
move configenv %BACKUP_DIR%
move install.bat %BACKUP_DIR%
@REM move run_videodownload.bat %BACKUP_DIR%


:: Check the move operation success
if errorlevel 1 (
    echo Failed to move the files. Aborting.
    exit /b 1
)

:: Run PyInstaller
echo Running PyInstaller...
python "c:\Users\wuxia\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\PyInstaller\__main__.py" video_downloader.spec

:: Check the PyInstaller operation success
if errorlevel 1 (
    echo Failed to run PyInstaller. Aborting.
    exit /b 1
)

echo Restoring config files to working directory...
move "%BACKUP_DIR%\config.env" ".\"
move "%BACKUP_DIR%\configenv" ".\"
move "%BACKUP_DIR%\install.bat" ".\"
@REM move "%BACKUP_DIR%\run_videodownload.bat" ".\"

echo Build process completed successfully.

:: Define the path to the configenv, install.bat, and executable, and ffmpeg files
set CONFIGENV_PATH=%WORK_DIR%\configenv
set INSTALL_PATH=%WORK_DIR%\install.bat
set EXE_PATH=%WORK_DIR%\dist\cnn10vd.exe
set FFMPEG_PATH=%WORK_DIR%\bin\ffmpeg.exe
@REM set RUN_VIDEODOWNLOAD=%WORK_DIR%\run_videodownload.bat

:: Define the name of the zip file and second zip file
set ZIP_FILE=%BACKUP_DIR%\release.zip
set RELEASEFFMPEG_ZIP=%BACKUP_DIR%\releaseffmpeg.zip

:: Check if the executable file exists
if not exist %EXE_PATH% (
    echo The executable file does not exist. Aborting.
    exit /b 1
)
:: Check if the configenv file exists
if not exist %CONFIGENV_PATH% (
    echo The configenv file does not exist. Aborting.
    exit /b 1
)
:: Check if the install.bat file exists
if not exist %INSTALL_PATH% (
    echo The install.bat file does not exist. Aborting.
    exit /b 1
)
:: Check if the ffmpeg executable file exists
if not exist %FFMPEG_PATH% (
    echo The ffmpeg executable file does not exist. Aborting.
    exit /b 1
)
@REM :: Check if the run_videodownload executable file exists
@REM if not exist %RUN_VIDEODOWNLOAD% (
@REM     echo The run_videodownload bat file does not exist. Aborting.
@REM     exit /b 1
@REM )

:: Create the zip file
echo Creating zip file...
:: Add a delay to ensure the file is no longer in use
timeout /t 5
@REM powershell -command "Compress-Archive -Path '%CONFIGENV_PATH%','%INSTALL_PATH%','%EXE_PATH%','%RUN_VIDEODOWNLOAD%' -DestinationPath '%ZIP_FILE%' -Force"
powershell -command "Compress-Archive -Path '%CONFIGENV_PATH%','%INSTALL_PATH%','%EXE_PATH%' -DestinationPath '%ZIP_FILE%' -Force"

:: Check the powershell operation success
if errorlevel 1 (
    echo Failed to create the zip file. Aborting.
    exit /b 1
)

echo Zip file created successfully at %ZIP_FILE%.

:: Create the second zip file
echo Creating second zip file...
:: Add a delay to ensure the file is no longer in use
timeout /t 5
@REM powershell -command "Compress-Archive -Path '%FFMPEG_PATH%', '%CONFIGENV_PATH%','%INSTALL_PATH%','%EXE_PATH%','%RUN_VIDEODOWNLOAD%' -DestinationPath '%RELEASEFFMPEG_ZIP%' -Force"
powershell -command "Compress-Archive -Path '%FFMPEG_PATH%', '%CONFIGENV_PATH%','%INSTALL_PATH%','%EXE_PATH%' -DestinationPath '%RELEASEFFMPEG_ZIP%' -Force"

:: Check the Compress-Archive operation success
if errorlevel 1 (
    echo Failed to create the second zip file. Aborting.
    exit /b 1
)

echo Second zip file created successfully at %RELEASEFFMPEG_ZIP%.

endlocal