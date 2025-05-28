import os
import sys

from src.entity.artifact_entity import ModelTrainerArtifact
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.cloud_storage.aws_storage import S3Operation
from src.constants import *


class ModelPusher:
    def __init__(self,  model_trainer_artifact: ModelTrainerArtifact):
        self.model_trainer_artifact = model_trainer_artifact
        self.s3 = S3Operation()
    
    def initiate_model_pusher(self):

        """
        Method Name :   initiate_model_pusher

        Description :   This method initiates model pusher. 
        
        Output      :    Model pusher artifact 
        """
        logging.info("Entered initiate_model_pusher method of Modelpusher class")
        try:
            # Uploading the best model to s3 bucket
            self.s3.upload_file(
                from_filename=self.model_trainer_artifact.trained_model_path,
                to_filename=TRAINED_MODEL_NAME,
                bucket_name=AWS_BUCKET_NAME,
                remove=False,
            )
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")


        except Exception as e:
            raise CustomException(e, sys)   
