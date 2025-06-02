import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.components.model_evaluation import ModelEvaluation
from src.exception.exception import CustomException



class ModelEvalPipe:
    def __init__(self,data_transform_artifact: DataTransformationArtifact,model_trainer_artifact:ModelTrainerArtifact):
        self.model_train_artifact=model_trainer_artifact
        self.model_Eval_config=ModelEvaluationConfig()
        self.data_transform_artifact=data_transform_artifact

    def main(self):
        try:
            model_eval=ModelEvaluation(data_transformation_artifact=self.data_transform_artifact,model_trainer_artifact=self.model_train_artifact,model_evaluation_config=self.model_Eval_config)
            model_Eval_Artifact=model_eval.initiate_model_evaluation()
            return model_Eval_Artifact
        except Exception as e:
            raise CustomException(e,sys)