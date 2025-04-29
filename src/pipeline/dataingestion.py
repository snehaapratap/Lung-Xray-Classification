import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import DataIngestionConfig
from src.components.data_ingestion import DataIngestion
from src.logger.custom_logging import logger
from src.exception.exception import CustomException


class DataIngestionPipe:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def main(self):
        try:

            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
   