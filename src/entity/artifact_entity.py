from dataclasses import dataclass
from torch.utils.data.dataloader import DataLoader

@dataclass
class DataIngestionArtifact:
    trained_file_path: str

    validation_file_path: str
