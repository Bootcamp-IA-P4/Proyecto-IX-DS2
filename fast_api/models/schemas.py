from pydantic import BaseModel
from typing import Literal
import torch.nn as nn
import torch.nn.functional as F

class InputData(BaseModel):
    gender: Literal[0, 1]
    age: int
    hypertension: Literal[0, 1]
    heart_disease: Literal[0, 1]
    ever_married: Literal[0, 1]
    Residence_type: Literal[0, 1]
    avg_glucose_level: float
    height: int
    weight: int
    work_type: Literal["Govt_job", "Private", "Self-employed", "children"]
    smoking_status: Literal["Unknown", "formerly smoked", "never smoked", "smokes"]

IMG_SIZE = 224

class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv_block = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc_block = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * (IMG_SIZE // 4) * (IMG_SIZE // 4), 224),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(224, num_classes)
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.fc_block(x)
        return x