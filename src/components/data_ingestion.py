
# from src.cloud_storage.aws_storage import S3Operation
from src.constants import *
import os,sys
from io import BytesIO
from PIL import Image
from sklearn.model_selection import train_test_split
from src.data_access.image_data import Image_Data
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception.exception import CustomException
from src.logger.custom_logging import logging



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def download_images_from_mongodb(self):
        try:
            image_data = Image_Data()
            images = image_data.fetch_images_as_bytes(self.config.collection_name)
            labeled_images = []
            for image_bytes, label in images:
                label = 'NORMAL' if 'NORMAL' in label else 'PNEUMONIA'
                labeled_images.append((image_bytes, label))
                
            logging.info(f"Downloaded {len(labeled_images)} images from MongoDB.")
            return labeled_images
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_images(self, image_tuples, save_dir):
        try:
            for idx, (image_bytes, label) in enumerate(image_tuples):
                if label not in ["NORMAL", "PNEUMONIA"]:
                    logging.warning(f"Unexpected label: {label}")
                    label = "UNKNOWN"  
            
                label_dir = os.path.join(save_dir, label)  
                os.makedirs(label_dir, exist_ok=True)  

                image = Image.open(BytesIO(image_bytes)).convert("RGB")
                image_path = os.path.join(label_dir, f"{label}_{idx}.jpg")
                image.save(image_path)

            logging.info(f"Saved {len(image_tuples)} images to {save_dir}")
        except Exception as e:
            raise CustomException(e, sys)

    def split_data_train_test(self, image_data):
        try:
            train_data, test_data = train_test_split(
                image_data,
                test_size=self.config.train_test_split_ratio,
                random_state=42
            )
            logging.info("Performed train/test split.")

            self.save_images(train_data, self.config.train_data_path)
            self.save_images(test_data, self.config.val_data_path)

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            image_data = self.download_images_from_mongodb()
            self.split_data_train_test(image_data)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.config.train_data_path,
                validation_file_path=self.config.val_data_path
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys)
