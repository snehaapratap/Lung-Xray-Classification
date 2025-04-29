from dataclasses import dataclass
from torch.utils.data.dataloader import DataLoader

@dataclass
class DataIngestionArtifact:
    trained_file_path: str

    validation_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_train_object: DataLoader

    transformed_val_object: DataLoader

    train_transform_file_path: str

    val_transform_file_path: str



@dataclass
class ModelTrainerArtifact:
    trained_model_path: str