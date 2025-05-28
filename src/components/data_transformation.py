import os
import sys
from typing import Tuple
from torch.utils.data import WeightedRandomSampler
from collections import Counter
import joblib
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,data_transformation_config: DataTransformationConfig,data_ingestion_artifact: DataIngestionArtifact,):
        self.data_transform_config=data_transformation_config
        self.data_ingestion_artifact=data_ingestion_artifact



    def transforming_training_data(self) -> transforms.Compose:
        try:
            logging.info(
                "Entered the transforming_training_data method of Data transformation class"
            )

            train_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transform_config.RESIZE),
                    transforms.CenterCrop(self.data_transform_config.CENTERCROP),
                    transforms.ColorJitter(
                        **self.data_transform_config.color_jitter_transforms
                    ),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(
                        self.data_transform_config.RANDOMROTATION
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transform_config.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_training_data method of Data transformation class"
            )

            return train_transform

        except Exception as e:
            raise CustomException(e, sys)
        
    def transforming_validation_data(self) -> transforms.Compose:
        logging.info(
            "Entered the transforming_testing_data method of Data transformation class"
        )

        try:
            test_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transform_config.RESIZE),
                    transforms.CenterCrop(self.data_transform_config.CENTERCROP),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transform_config.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_testing_data method of Data transformation class"
            )

            return test_transform

        except Exception as e:
            raise CustomException(e, sys)
            
    def data_loader(self, train_transform: transforms.Compose, test_transform: transforms.Compose) -> Tuple[DataLoader, DataLoader]:
        try:
            logging.info("Entered the data_loader method of Data transformation class")
            print("Train Path:", self.data_ingestion_artifact.trained_file_path)
            print("Val Path:", self.data_ingestion_artifact.validation_file_path)

            train_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifact.trained_file_path),
                transform=train_transform,
            )

            val_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifact.validation_file_path),
                transform=test_transform,
            )

            logging.info("Created train data and test data paths")

            # Get the class labels of each image
            targets = [sample[1] for sample in train_data.samples]
            class_counts = Counter(targets)

        # Log class distribution
            logging.info(f"Class Distribution in Training Set: {class_counts}")

        # Compute class weights and sample weights
            class_weights = {cls: 1.0 / count for cls, count in class_counts.items()}
            sample_weights = [class_weights[label] for label in targets]

        # Create Weighted Sampler
            sampler = WeightedRandomSampler(
            weights=sample_weights,
            num_samples=len(sample_weights),
            replacement=True
            )


            train_loader: DataLoader = DataLoader(
                train_data, 
                sampler=sampler,
                # **self.data_transform_config.data_loader_params,sampler=sampler,
                batch_size=self.data_transform_config.data_loader_params["batch_size"],
                pin_memory=self.data_transform_config.data_loader_params["pin_memory"],
                num_workers=0
            )

            val_loader: DataLoader = DataLoader(
                val_data, 
                shuffle=False,
                batch_size=self.data_transform_config.data_loader_params["batch_size"],
                pin_memory=self.data_transform_config.data_loader_params["pin_memory"],
                num_workers=0
    
            )

            logging.info("Exited the data_loader method of Data transformation class")

            return train_loader, val_loader

        except Exception as e:
            raise CustomException(e, sys)        
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(
                "Entered the initiate_data_transformation method of Data transformation class"
            )

            train_transform: transforms.Compose = self.transforming_training_data()

            val_transform: transforms.Compose = self.transforming_validation_data()

            os.makedirs(self.data_transform_config.artifact_dir, exist_ok=True)

            joblib.dump(
                train_transform, self.data_transform_config.train_transforms_file
            )

            joblib.dump(
                val_transform, self.data_transform_config.val_transforms_file
            )

            train_loader, val_loader = self.data_loader(
                train_transform=train_transform, test_transform=val_transform
            )

            data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                transformed_train_object=train_loader,
                transformed_val_object=val_loader,
                train_transform_file_path=self.data_transform_config.train_transforms_file,
                val_transform_file_path=self.data_transform_config.val_transforms_file,
            )

            logging.info(
                "Exited the initiate_data_transformation method of Data transformation class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys)    