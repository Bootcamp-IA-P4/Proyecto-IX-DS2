import os
import pytest
from fast_api.core import model_loader

def test_load_joblib_model_success():
    # Ruta absoluta al archivo para evitar problemas relativos
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "model.pkl")
    model = model_loader.load_joblib_model(model_path)
    assert model is not None
    assert hasattr(model, "predict")

def test_load_cnn_model_success():
    model_path = os.path.join(os.path.dirname(__file__), "..", "data", "cnn_pytorch.pth")
    model = model_loader.load_cnn_model(model_path)
    assert model is not None
    # Como es un modelo PyTorch, aseguramos que está en modo eval
    assert model.training is False

def test_load_joblib_model_file_not_found():
    with pytest.raises(Exception):
        model_loader.load_joblib_model("non_existent_file.pkl")

def test_load_cnn_model_file_not_found():
    with pytest.raises(Exception):
        model_loader.load_cnn_model("non_existent_file.pth")