# /backend_model/api/imgs.py
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import torch
from torchvision import transforms

# --- Import corregido ---
from backend_model.core.model_loader import load_cnn_model
import logging

img_router = APIRouter()
model = load_cnn_model()
IMG_SIZE = 224

# Transformación para las imágenes
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

# La ruta ahora es `/infer/image` para que sea consistente
@img_router.post("/infer/image") 
async def infer_image(file: UploadFile = File(...)):
    """
    Esta función SÓLO se encarga de la predicción.
    No habla con Supabase, no guarda nada en la BBDD.
    Recibe un archivo, devuelve un JSON con el resultado.
    """
    try:
        # Leer y transformar la imagen
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)
        logging.info(f"Modelo de imagen: procesando {file.filename}")

        # Predicción
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            prediction = int(torch.argmax(probabilities, dim=1).item())
            probability = float(probabilities[0][prediction].item())

        logging.info(f"Modelo de imagen: predicción completada.")
        
        # Devuelve un resultado simple y crudo.
        return {
            "prediction": prediction,
            "probability": round(probability, 4)
        }

    except Exception as e:
        logging.error(f"Error en el modelo de imagen: {str(e)}")
        # En producción, podrías querer ser menos explícito con el error
        raise HTTPException(status_code=500, detail="Error interno al procesar la imagen.")