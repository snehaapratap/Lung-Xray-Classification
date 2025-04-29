import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights

class EfficientNetV2S(nn.Module):
    def __init__(self, num_classes=2):
        super(EfficientNetV2S, self).__init__()
        
        self.model = efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.DEFAULT)
        in_features = self.model.classifier[1].in_features
        
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=0.4, inplace=True),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        x = self.model(x)
        return F.log_softmax(x, dim=-1)


