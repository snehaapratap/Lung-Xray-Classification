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