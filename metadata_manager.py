# metadata_manager.py v1.2.0

# Description: Manages the storage, retrieval, and querying of video metadata.

import json
import os
import logging
from typing import Optional

logger = logging.getLogger('metadata_manager')

class MetadataManager:

    def __init__(self, config):
        """Initialize the MetadataManager with a specific metadata file."""
        self.metadata_file = config["METADATA_FILE"]
        if not os.path.exists(self.metadata_file):
            os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
            self._initialize_metadata_file()

    def _initialize_metadata_file(self):
        """Initialize an empty metadata file."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump([], f)
        except Exception as e:
            logger.error(f"Error initializing metadata file: {e}")
            raise

    def save_or_update_metadata(self, metadata: dict):
        """Save or update a video's metadata in the metadata file."""
        try:
            data = self.get_all_metadata()

            existing_metadata = [item for item in data if item['id'] == metadata['id']]
            if existing_metadata:
                index = data.index(existing_metadata[0])
                data[index] = metadata
            else:
                data.append(metadata)

            with open(self.metadata_file, 'w') as f:
                json.dump(data, f)

            logger.info(f"Stored/Updated metadata for video: {metadata['title']}")

        except Exception as e:
            logger.error(f"Error saving/updating metadata for video {metadata['title']}: {e}")
            raise

    def get_all_metadata(self) -> list:
        """Retrieve all video metadata from the metadata file."""
        try:
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error retrieving all metadata: {e}")
            raise

    def query_metadata(self, video_id: str) -> Optional[dict]:
        """Query metadata based on a video ID."""
        try:
            data = self.get_all_metadata()
            for item in data:
                if item['id'] == video_id:
                    return item
            return None
        except Exception as e:
            logger.error(f"Error querying metadata for video ID {video_id}: {e}")
            raise
