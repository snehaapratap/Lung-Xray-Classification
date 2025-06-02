import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import DataTransformationConfig
from src.pipeline.dataingestion import DataIngestionPipe
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_transformation import DataTransformation
from src.logger.custom_logging import logger
from src.exception.exception import CustomException



class DataTransfromPipe:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact):
        self.data_transform_config = DataTransformationConfig()
        self.data_ingestion_artifact=data_ingestion_artifact

    def main(self):
        try:

            data_transform=DataTransformation(self.data_transform_config,self.data_ingestion_artifact)
            data_transform_artifact = data_transform.initiate_data_transformation()
            return data_transform_artifact
        except Exception as e:
            raise CustomException(e,sys)

 