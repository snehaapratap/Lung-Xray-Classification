import sys
from typing import Tuple

import torch
from torch.nn import CrossEntropyLoss, Module
from torch.optim import Adam, Optimizer
from torch.utils.data import DataLoader

from src.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelEvaluationArtifact,
    ModelTrainerArtifact,
)
from src.entity.config_entity import ModelEvaluationConfig
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.constants import *
from src.model.arch import EfficientNetV2S


class ModelEvaluation:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_evaluation_config: ModelEvaluationConfig,
        model_trainer_artifact: ModelTrainerArtifact,
    ):

        self.data_transformation_artifact = data_transformation_artifact

        self.model_evaluation_config = model_evaluation_config

        self.model_trainer_artifact = model_trainer_artifact

    def configuration(self) -> Tuple[DataLoader, Module, float, Optimizer]:
        logging.info("Entered the configuration method of Model evaluation class")

        try:
            validation_dataloader: DataLoader = (
                self.data_transformation_artifact.transformed_val_object
            )

            model: Module = EfficientNetV2S()

            model.load_state_dict(torch.load(self.model_trainer_artifact.trained_model_path,map_location=self.model_evaluation_config.device))

            model.to(self.model_evaluation_config.device)

        #     normal_count = 28   # Class 0: NORMAL
        #     pneumonia_count = 140  # Class 1: PNEUMONIA

        # # Compute pos_weight = negative / positive
        #     pos_weight_value = normal_count / pneumonia_count
        #     pos_weight = torch.tensor([pos_weight_value]).to(self.model_evaluation_config.device)

        # Binary classification loss with class imbalance
            # cost: torch.nn.Module = torch.nn.BCEWithLogitsLoss(pos_weight=pos_weight)


            cost: Module = CrossEntropyLoss()

            

            model.eval()

            logging.info("Exited the configuration method of Model evaluation class")

            return validation_dataloader, model, cost

        except Exception as e:
            raise CustomException(e, sys)    
        
    def validation_net(self) -> float:
        logging.info("Entered the val_net method of Model evaluation class")

        try:
            test_dataloader, net, cost = self.configuration()

            with torch.no_grad():
                holder = []

                for _, data in enumerate(test_dataloader):
                    images = data[0].to(self.model_evaluation_config.device)

                    labels = data[1].to(self.model_evaluation_config.device)

                    output = net(images)

                    loss = cost(output, labels)

                    predictions = torch.argmax(output, 1)

                    for i in zip(images, labels, predictions):
                        h = list(i)

                        holder.append(h)

                    logging.info(f"Actual_Labels : {labels}     Predictions : {predictions}     labels : {loss.item():.4f}")

                    self.model_evaluation_config.validation_loss += loss.item()

                    self.model_evaluation_config.validation_accuracy += (
                        (predictions == labels).sum().item()
                    )

                    self.model_evaluation_config.total_batch += 1

                    self.model_evaluation_config.total += labels.size(0)

                    logging.info(
                    f"Model  -->   Loss : {self.model_evaluation_config.validation_loss/ self.model_evaluation_config.total_batch} Accuracy : {(self.model_evaluation_config.validation_accuracy / self.model_evaluation_config.total) * 100} %"
                    )

            accuracy = (self.model_evaluation_config.validation_accuracy/ self.model_evaluation_config.total) * 100

            logging.info("Exited the test_net method of Model evaluation class")

            return accuracy

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        logging.info(
            "Entered the initiate_model_evaluation method of Model evaluation class"
        )

        try:
            accuracy = self.validation_net()

            model_evaluation_artifact: ModelEvaluationArtifact = (
                ModelEvaluationArtifact(model_accuracy=accuracy)
            )

            logging.info(
                "Exited the initiate_model_evaluation method of Model evaluation class"
            )

            return model_evaluation_artifact

        except Exception as e:
            raise CustomException(e, sys)    