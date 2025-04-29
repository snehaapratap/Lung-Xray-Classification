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
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP,"data_ingestion")
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
