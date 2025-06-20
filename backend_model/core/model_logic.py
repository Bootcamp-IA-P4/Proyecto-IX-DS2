# /backend_model/core/model_logic.py
import torch
from PIL import Image
from io import BytesIO
from torchvision import transforms

from .model_loader import load_cnn_model # Ya no necesitamos cargar el modelo de sklearn aquí

# Carga el modelo de CNN al inicio del módulo
cnn_model = load_cnn_model()

# --- SOLO LÓGICA DE IMAGEN ---

# Transformaciones de imagen
IMG_SIZE = 224
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

def predict_image_data(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = cnn_model(input_tensor)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        prediction_class = int(torch.argmax(probabilities, dim=1).item())
        probability = float(probabilities[0][prediction_class].item())
    
    return {"prediction": prediction_class, "probability": probability}

# --- HEMOS ELIMINADO la función `predict_tabular_data` y la carga de `skl_model` ---
# --- porque la lógica correcta está en `services/prediction.py` ---