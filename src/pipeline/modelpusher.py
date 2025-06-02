import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.components.model_pusher import ModelPusher
from src.exception.exception import CustomException
from dotenv import load_dotenv

load_dotenv()


class ModelPusherPipe:
    def __init__(self,model_trainer_artifact):
        self.model_trainer_artifact=model_trainer_artifact

        
    def main(self):
        try:
            model_push=ModelPusher(model_trainer_artifact=self.model_trainer_artifact)
            model_push_artifact=model_push.initiate_model_pusher()
            return model_push_artifact
        except Exception as e:
            raise CustomException(e,sys)