# /backend_model/core/model_loader.py
import os
import joblib
import torch
import logging

from backend_model.core.model_definition import SimpleCNN
# from logs.logger_setup import setup_logging  # Descomenta si usas tu setup de logging
# setup_logging()

# Definimos el directorio raíz del SERVICIO
SERVICE_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_joblib_model():
    """Carga el modelo de Scikit-learn guardado con joblib."""
    model_path = os.path.join(SERVICE_ROOT_DIR, "model.pkl")
    
    try:
        model = joblib.load(model_path)
        logging.info(f"Modelo .pkl cargado correctamente desde: {model_path}")
        return model
    except FileNotFoundError:
        logging.error(f"No se encontró el modelo .pkl en la ruta: {model_path}")
        raise


def load_cnn_model():
    """Carga el modelo de PyTorch."""
    model_path = os.path.join(SERVICE_ROOT_DIR, "cnn_pytorch.pth")

    try:
        model = SimpleCNN(num_classes=2)
        device = torch.device("cpu")
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        logging.info(f"Modelo .pth cargado correctamente desde: {model_path}")
        return model
    except FileNotFoundError:
        logging.error(f"No se encontró el modelo .pth en la ruta: {model_path}")
        raise