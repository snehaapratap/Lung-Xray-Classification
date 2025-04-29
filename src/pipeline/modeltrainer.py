import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import ModelTrainerConfig
from src.pipeline.dataingestion import DataIngestionPipe
from src.entity.artifact_entity import DataTransformationArtifact
from src.components.model_trainer import ModelTrainer
from src.exception.exception import CustomException



class ModelTrainerPipe:
    def __init__(self,data_transform_artifact: DataTransformationArtifact):
        self.model_trainer_config = ModelTrainerConfig()
        self.data_transform_artifact=data_transform_artifact

    def main(self):
        try:

            model_trainer=ModelTrainer(data_transformation_artifact=self.data_transform_artifact,model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
