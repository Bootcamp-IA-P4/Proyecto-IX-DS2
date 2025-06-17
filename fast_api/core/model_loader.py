import os, joblib
import torch
from fast_api.models.schemas import SimpleCNN

def load_joblib_model(model_path=None):
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "model.pkl")

    model = joblib.load(model_path)
    return model


def load_cnn_model(model_path=None):
    if model_path is None:
        model_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cnn_pytorch.pth")

    model = SimpleCNN(num_classes=2)
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model