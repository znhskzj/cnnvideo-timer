# metadata_manager.py v1.1.0
# Description: Manages the storage, retrieval, and querying of video metadata.

import json
import os
import logging

logger = logging.getLogger('metadata_manager')

class MetadataManager:

    def __init__(self, metadata_file="log/metadata.json"):
        self.metadata_file = metadata_file
        # 如果文件不存在，创建一个空的
        if not os.path.exists(metadata_file):
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)  # Ensure the directory exists
            try:
                with open(metadata_file, 'w') as f:
                    json.dump([], f)
                    # json.dump({}, f)
            except Exception as e:
                logger.error(f"Error initializing metadata file: {e}")
                raise e
            
    def save_or_update_metadata(self, metadata):
        """保存或更新视频的元数据到文件中。"""
        try:
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)

            # 打印检索到的元数据
            print(f"Retrieved metadata for video {metadata['title']}:")
            print(json.dumps(metadata, indent=4, sort_keys=True))  # 以格式化的JSON格式打印

            # Check if the video with the same ID already exists in the metadata.
            existing_metadata = [item for item in data if item['id'] == metadata['id']]
            if existing_metadata:
                # If the video with the same ID exists, update its metadata.
                index = data.index(existing_metadata[0])
                data[index] = metadata
            else:
                # If not, append the new metadata.
                data.append(metadata)

            with open(self.metadata_file, 'w') as f:
                json.dump(data, f)

            logger.info(f"Stored/Updated metadata for video: {metadata['title']}")

        except Exception as e:
            logger.error(f"Error saving/updating metadata for video {metadata['title']}: {e}")
            raise e
        
    def get_all_metadata(self):
        """Retrieve all video metadata from the metadata file."""
        try:
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error retrieving all metadata: {e}")
            raise e
        
    def query_metadata(self, video_id):
        """根据视频ID查询元数据"""
        try:
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
            
            for item in data:
                if item['id'] == video_id:
                    return item
            return None  # 如果没有找到对应的元数据
        except Exception as e:
            logger.error(f"Error querying metadata for video ID {video_id}: {e}")
            raise e
