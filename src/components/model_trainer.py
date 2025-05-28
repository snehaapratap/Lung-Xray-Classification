import os
import sys

import bentoml
import joblib
import torch
import torch.nn.functional as F
from torch.nn import Module
from torch.optim import Optimizer
from torch.optim.lr_scheduler import StepLR, _LRScheduler
from tqdm import tqdm

from src.constants import *
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from src.entity.config_entity import ModelTrainerConfig
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.model.arch import EfficientNetV2S


class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact,model_trainer_config: ModelTrainerConfig,):
        self.model_trainer_config: ModelTrainerConfig = model_trainer_config

        self.data_transformation_artifact: DataTransformationArtifact = data_transformation_artifact

        self.model: Module = EfficientNetV2S(num_classes=2)

    def train(self,optimizer:Optimizer):
        logging.info("Entered the train method of Model trainer class")
        try:
            self.model.train()
            pbar = tqdm(self.data_transformation_artifact.transformed_train_object)  # to show progress bar

            correct: int = 0

            processed = 0

            for batch_idx,(data,target)in enumerate(pbar):
                data, target = data.to(DEVICE), target.to(DEVICE)
                print(torch.unique(target))

                # Initialization of gradient
                optimizer.zero_grad()

                y_pred=self.model(data)

                loss=F.nll_loss(y_pred,target)

                loss.backward()

                optimizer.step()

                pred=y_pred.argmax(dim=1, keepdim=True)

                correct += pred.eq(target.view_as(pred)).sum().item()

                processed += len(data)

                pbar.set_description(
                    desc=f"Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}"
                )

            logging.info("Exited the train method of Model trainer class")



        except Exception as e:
            raise CustomException(e,sys)    


    def validation(self):
        logging.info("Entered the Validation method of Model trainer class")

        try:
        
            self.model.eval()

            val_loss: float = 0.0

            correct: int = 0

            with torch.no_grad():
                for (data,target) in self.data_transformation_artifact.transformed_val_object:
                    data, target = data.to(DEVICE), target.to(DEVICE)

                    output = self.model(data)

                    val_loss += F.nll_loss(output, target, reduction="sum").item()

                    pred = output.argmax(dim=1, keepdim=True)

                    correct += pred.eq(target.view_as(pred)).sum().item()

                    val_loss /= len(
                    self.data_transformation_artifact.transformed_val_object.dataset
                )

                print( "Validation set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n".format(val_loss,correct,
                        len(self.data_transformation_artifact.transformed_val_object.dataset),
                        100.0 * correct/ len(self.data_transformation_artifact.transformed_val_object.dataset),
                    )
                )

            logging.info("Validation set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)".format(val_loss,correct,len(self.data_transformation_artifact.transformed_val_object.dataset),
                    100.0* correct/ len(self.data_transformation_artifact.transformed_val_object.dataset),))

            logging.info("Exited the Validation method of Model trainer class")


        except Exception as e:
            raise CustomException(e,sys)    


    def initate_model_trainer(self):
        try:
            logging.info('Entered Initate Model trainer function')
            model:Module=self.model.to(self.model_trainer_config.device)

            optimizer: Optimizer = torch.optim.Adam(model.parameters(), **self.model_trainer_config.optimizer_params)


            scheduler: _LRScheduler = StepLR(
                optimizer=optimizer, **self.model_trainer_config.scheduler_params
            )

            for epoch in range(1, self.model_trainer_config.epochs + 1):
                print("Epoch : ", epoch)

                self.train(optimizer=optimizer)

                optimizer.step()

                scheduler.step()

                self.validation()

            os.makedirs(self.model_trainer_config.artifact_dir, exist_ok=True)

            torch.save(model.state_dict(), self.model_trainer_config.trained_model_path)

            train_transforms_obj = joblib.load(
                self.data_transformation_artifact.train_transform_file_path
            )

            bentoml.pytorch.save_model(
                name=self.model_trainer_config.trained_bentoml_model_name,
                model=model,
                custom_objects={
                    self.model_trainer_config.train_transforms_key:train_transforms_obj
                }
            )
            model_trainer_artifact: ModelTrainerArtifact = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.trained_model_path
            )

            logging.info(
                "Exited the initiate_model_trainer method of Model trainer class"
            )

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e,sys)    


