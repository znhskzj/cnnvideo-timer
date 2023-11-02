import os
import sys
import zipfile
import requests
from subprocess import check_call

def download_ffmpeg():
    url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
    response = requests.get(url, stream=True)
    with open('ffmpeg.zip', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def unzip_ffmpeg():
    with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
        zip_ref.extractall('.')

def add_to_path():
    ffmpeg_path = os.path.abspath('./ffmpeg/bin')
    existing_path = os.environ.get('PATH', '')
    new_path = f"{ffmpeg_path};{existing_path}"
    check_call(f'setx PATH "{new_path}"', shell=True)

def main():
    if not os.path.exists('./ffmpeg/bin/ffmpeg.exe'):
        print("FFmpeg not found, downloading...")
        download_ffmpeg()
        print("Extracting FFmpeg...")
        unzip_ffmpeg()
    print("Adding FFmpeg to PATH...")
    add_to_path()
    print("Installation complete!")

if __name__ == "__main__":
    main()
