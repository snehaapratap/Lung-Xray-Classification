from dotenv import load_dotenv
from typing import List
from datetime import datetime
import os,torch
load_dotenv()
uri = os.getenv('MONGODB_URI')


AWS_BUCKET_NAME='lung-xray-yt'
MONGODB_URI=uri
db_name='akash'
DATABASE_NAME='lung_xray_db'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=.20
collection_name="fs.files"

TIMESTAMP: datetime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Data Ingestion Constants
ARTIFACT_DIR: str = "artifacts"


# data trasnforamtion
CLASS_LABEL_1: str = "NORMAL"

CLASS_LABEL_2: str = "PNEUMONIA"

BRIGHTNESS: int = 0.20

CONTRAST: int = 0.20

SATURATION: int = 0.25

HUE: int = 0.1


IMAGE_SHAPE = 224

CENTERCROP: int = 224

RANDOMROTATION: int = 30

NORMALIZE_LIST_1: List[int] = [0.485, 0.456, 0.406]

NORMALIZE_LIST_2: List[int] = [0.229, 0.224, 0.225]

TRAIN_TRANSFORMS_KEY: str = "xray_train_transforms"

TRAIN_TRANSFORMS_FILE: str = "train_transforms.pkl"

VAL_TRANSFORMS_FILE: str = "validation_transforms.pkl"

BATCH_SIZE: int = 8

SHUFFLE: bool = True

PIN_MEMORY: bool = True





TRAINED_MODEL_DIR: str = "model_training"

TRAINED_MODEL_NAME: str = "model.pt"

DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

STEP_SIZE: int = 6

GAMMA: int = 0.5

EPOCH: int = 3

BENTOML_MODEL_NAME: str = "xray_model"

BENTOML_SERVICE_NAME: str = "xray_service"

BENTOML_ECR_URI: str = "lung-xray"

PREDICTION_LABEL: dict = {"0": CLASS_LABEL_1, 1: CLASS_LABEL_2}


AWS_Model_URI='s3://lung-xray-yt/model.pt'
