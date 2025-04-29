import sys
from typing import List, Tuple, Optional
from pymongo import MongoClient
import gridfs
from src.configuraion.mongodb_connection import MongoDBConnection
from src.constants import DATABASE_NAME
from src.exception.expection import CustomException


class Image_Data:
    def __init__(self):
        try:
            self.client = MongoDBConnection(Databse_name=DATABASE_NAME)
            self.database = self.client.database
            self.fs = gridfs.GridFS(self.client.database)
        except Exception as e:
            raise CustomException(e, sys)

    def fetch_images_as_bytes(self, collection_name: Optional[str] = None) -> List[Tuple[bytes, str]]:
        """
        Fetch images from GridFS and return a list of tuples: (image_bytes, label)
        Assumes each file in GridFS has a 'label' field in metadata.
        """
        try:
            files = self.fs.find()
            data = []

            for file in files:
                image_bytes = file.read()
                label = file.filename.split("/")[0]  
                data.append((image_bytes, label))

            return data

        except Exception as e:
            raise CustomException(e, sys)
