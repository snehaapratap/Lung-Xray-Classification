import os
import sys
import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from pymongo.server_api import ServerApi
from src.constants import DATABASE_NAME
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('MONGODB_URI')

ca=certifi.where()

class MongoDBConnection:
    client = None
    def __init__(self,Databse_name:str=DATABASE_NAME):
        try:
            if MongoDBConnection.client is None:
                if uri is None:
                    raise CustomException("MONGODB_URL_KEY is None",sys)
                
                MongoDBConnection.client=MongoClient(uri,server_api=ServerApi('1'))
            self.client=MongoDBConnection.client
            self.database_name=Databse_name
            self.database=self.client[self.database_name] 
            logging.info("MongoDB connection successful.")   
        except Exception as e:
            raise CustomException(e,sys) 