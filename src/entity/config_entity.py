import os
from dataclasses import dataclass, field
from typing import Tuple


from torch import device

from src.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.collection_name = collection_name
        self.train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        # self.training_image_dir = training_image_dir
        # self.validation_image_dir = validation_image_dir
        
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP,"data_ingestion")

        # self.data_path: str = os.path.join(self.artifact_dir, "data_ingestion")

        self.train_data_path: str = os.path.join(self.artifact_dir, "train")

        self.val_data_path: str = os.path.join(self.artifact_dir, "validation")

@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.color_jitter_transforms: dict = {
            "brightness": BRIGHTNESS,
            "contrast": CONTRAST,
            "saturation": SATURATION,
            "hue": HUE,
        }

        self.RESIZE: int = IMAGE_SHAPE
        # self.RESIZE: Tuple[int, int] = field(default_factory=lambda: IMAGE_SHAPE[:2])

        self.CENTERCROP: int = CENTERCROP

        self.RANDOMROTATION: int = RANDOMROTATION

        self.normalize_transforms: dict = {
            "mean": NORMALIZE_LIST_1,
            "std": NORMALIZE_LIST_2,
        }

        self.data_loader_params: dict = {
            "batch_size": BATCH_SIZE,
            "shuffle": SHUFFLE,
            "pin_memory": PIN_MEMORY,
        }

        self.artifact_dir: str = os.path.join(
            ARTIFACT_DIR, TIMESTAMP, "data_transformation"
        )

        self.train_transforms_file: str = os.path.join(
            self.artifact_dir, TRAIN_TRANSFORMS_FILE
        )

        self.val_transforms_file: str = os.path.join(
            self.artifact_dir, VAL_TRANSFORMS_FILE
        )

       
@dataclass
class ModelTrainerConfig:
    def __init__(self):
        self.artifact_dir: int = os.path.join(ARTIFACT_DIR, TIMESTAMP, "model_training")

        self.trained_bentoml_model_name: str = "xray_model"

        self.trained_model_path: int = os.path.join(
            self.artifact_dir, TRAINED_MODEL_NAME
        )

        self.train_transforms_key: str = TRAIN_TRANSFORMS_KEY

        self.epochs: int = EPOCH

        self.optimizer_params: dict = {"lr": 0.0001,"weight_decay": 5e-4}

        self.scheduler_params: dict = {"step_size": STEP_SIZE, "gamma": GAMMA}

        self.device: device = DEVICE

        
               
@dataclass
class ModelEvaluationConfig:
    def __init__(self):
        self.device: device = DEVICE

        self.validation_loss: int = 0

        self.validation_accuracy: int = 0

        self.total: int = 0

        self.total_batch: int = 0

        self.optimizer_params: dict = {"lr": 0.0001,"weight_decay": 5e-4}                


