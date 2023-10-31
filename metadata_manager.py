# metadata_manager.py v1.3.2

# Description: Manages the storage, retrieval, and querying of video metadata.

import json
import os
import logging
from typing import Optional
from config_loader import load_config

logger = logging.getLogger('metadata_manager')
config = load_config()

# 引入 youtube_metadata_checker 中的方法
from youtube_metadata_checker import get_metadata_from_api, get_metadata_from_yt_dlp

class MetadataManager:
    def __init__(self, config):
        self.metadata_file_path = config['METADATA_FILE']  # 获取元数据文件的路径

    def save_or_update_metadata(self, metadata):
        video_id = metadata.get('id')
        if video_id:
            all_metadata = self.get_all_metadata()
            all_metadata[video_id] = metadata
            with open(self.metadata_file_path, 'w', encoding='utf-8') as file:
                json.dump(all_metadata, file, ensure_ascii=False, indent=4)

    def get_all_metadata(self):
        if os.path.exists(self.metadata_file_path):
            with open(self.metadata_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def query_metadata(self, video_id):
        all_metadata = self.get_all_metadata()
        return all_metadata.get(video_id)

    def extract_and_save_additional_metadata(self, video_id):
        if self.default_metadata_extractor == 'api':
            additional_metadata = get_metadata_from_api(video_id)
        else:
            additional_metadata = get_metadata_from_yt_dlp(video_id)
        
        if additional_metadata:
            existing_metadata = self.query_metadata(video_id) or {}
            updated_metadata = {**existing_metadata, **additional_metadata}
            self.save_or_update_metadata(updated_metadata)
    
    def get_metadata_file_path(self, video_id):
        """生成元数据文件的路径"""
        return os.path.join(self.metadata_file_path, f"{video_id}.json")