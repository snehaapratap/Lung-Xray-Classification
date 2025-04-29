from dotenv import load_dotenv
from typing import List
from datetime import datetime
import os
import torch

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = 'lung_xray_db'
COLLECTION_NAME = "fs.files"

# Timestamp for artifact versioning
TIMESTAMP: datetime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Data Ingestion Constants
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.20

# Data Transformation Constants
CLASS_LABEL_1: str = "NORMAL"
CLASS_LABEL_2: str = "PNEUMONIA"
BRIGHTNESS: float = 0.20
CONTRAST: float = 0.20
SATURATION: float = 0.25
HUE: float = 0.1
IMAGE_SHAPE = 224
CENTERCROP: int = 224
RANDOMROTATION: int = 30
NORMALIZE_LIST_1: List[float] = [0.485, 0.456, 0.406]
NORMALIZE_LIST_2: List[float] = [0.229, 0.224, 0.225]

# Training Configuration
BATCH_SIZE: int = 8
SHUFFLE: bool = True
PIN_MEMORY: bool = True
STEP_SIZE: int = 6
GAMMA: float = 0.5
EPOCH: int = 3
DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Artifact Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
TRAINED_MODEL_PATH = os.path.join(ARTIFACTS_DIR, "trained_model.pth")
TRAIN_TRANSFORMS_FILE: str = os.path.join(ARTIFACTS_DIR, "train_transforms.pkl")
VAL_TRANSFORMS_FILE: str = os.path.join(ARTIFACTS_DIR, "validation_transforms.pkl")

# BentoML Configuration
BENTOML_MODEL_NAME: str = "lung_xray_classifier"
BENTOML_SERVICE_NAME: str = "xray_service"

# Prediction Labels
PREDICTION_LABEL: dict = {"0": CLASS_LABEL_1, "1": CLASS_LABEL_2}