
# from src.cloud_storage.aws_storage import S3Operation
from src.constants import *
import os,sys
from io import BytesIO
from PIL import Image
from sklearn.model_selection import train_test_split
from src.data_access.Image_data import Image_Data
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception.expection import CustomException
from src.logger.custom_logging import logging



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def download_images_from_mongodb(self):
        """
        Retrieve images from MongoDB using GridFS and return a list of (image_bytes, label) tuples.
        """
        try:
            image_data = Image_Data()
            # images = image_data.fetch_images_as_bytes(self.config.collection_name)
            # logging.info(f"Downloaded {len(images)} images from MongoDB.")
            # return images
            images = image_data.fetch_images_as_bytes(self.config.collection_name)
            labeled_images = []

            # Assume that label is embedded in the metadata or filename
            for image_bytes, label in images:
                # Extract the label from metadata or filename, assuming label is present in metadata
                # For this case, we assume labels are fetched from image metadata or filename
                label = 'NORMAL' if 'NORMAL' in label else 'PNEUMONIA'
                labeled_images.append((image_bytes, label))
                
            logging.info(f"Downloaded {len(labeled_images)} images from MongoDB.")
            return labeled_images
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_images(self, image_tuples, save_dir):
        """
        Save images to the given directory with subfolders by label.
        """
        # try:
        #     for idx, (image_bytes, label) in enumerate(image_tuples):
        #         label_dir = os.path.join(save_dir, label)
        #         os.makedirs(label_dir, exist_ok=True)
        #         image = Image.open(BytesIO(image_bytes)).convert("RGB")
        #         image_path = os.path.join(label_dir, f"{label}_{idx}.jpg")
        #         image.save(image_path)
        #     logging.info(f"Saved {len(image_tuples)} images to {save_dir}")
        # except Exception as e:
        #     raise CustomException(e, sys)
        # try:
        #     for idx, (image_bytes, label) in enumerate(image_tuples):
        #         label_dir = os.path.join(save_dir, label)  # Ensure class labels are used
        #         os.makedirs(label_dir, exist_ok=True)
            
        #         image = Image.open(BytesIO(image_bytes)).convert("RGB")
        #         image_path = os.path.join(label_dir, f"{label}_{idx}.jpg")
        #         image.save(image_path)

        #     logging.info(f"Saved {len(image_tuples)} images to {save_dir}")

        # except Exception as e:
        #     raise CustomException(e, sys)

        try:
            for idx, (image_bytes, label) in enumerate(image_tuples):
            # Ensure that the label is correct (e.g., 'NORMAL' or 'PNEUMONIA')
            # If the label is not correct, log it or assign a default class
                if label not in ["NORMAL", "PNEUMONIA"]:
                    logging.warning(f"Unexpected label: {label}")
                    label = "UNKNOWN"  # Default class if label is not valid
            
                label_dir = os.path.join(save_dir, label)  # Class subfolder
                os.makedirs(label_dir, exist_ok=True)  # Create class subfolder if it doesn't exist

            # Save the image to the corresponding class folder
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


# class DataIngestion:
#     def __init__(self):
#         pass

#     def get_data_from_s3(self):
#         try:
#             logging.info("Entered into get data from s3")
#             pass
#         except Exception as e:
#             raise CustomException(e,sys)

#     def initate_data_ingestion(self):
#         try:
#             logging.info("Initated data ingestion")
#             pass
#         except Exception as e:
#             raise CustomException(e,sys)