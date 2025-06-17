import os
import sys
import io
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import torch
from torchvision import transforms
from supabase import create_client

# importamos el modelo CNN
from fast_api.core.model_loader import load_cnn_model

# importamos la configuración de logging
import logging
from logs.logger_setup import setup_logging
# configuramos el logger
setup_logging()

# configuramos las variables de entorno de supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
# creamos el nombre del bucket
BUCKET_NAME = "stroke-images"
# creamos el router para las imágenes
img_router = APIRouter()
# creamos variable con el modelo PyTorch
model = load_cnn_model()

IMG_SIZE = 224

# Transformación para las imágenes
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

@img_router.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logging.error(f"Formato de imagen no válido: {file.filename}")
        raise HTTPException(status_code=400, detail="Formato de imagen no válido.")
    try:
        # Leer y transformar la imagen
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)
        logging.info(f"Imagen procesada: {file.filename}")

        # Predicción
        with torch.no_grad():
            output = model(input_tensor)
            logging.info(f"Predicción realizada para: {file.filename}")
            probabilities = torch.nn.functional.softmax(output, dim=1)
            prediction = int(torch.argmax(probabilities, dim=1).item())
            probability = float(probabilities[0][prediction].item())

        # Nombre de archivo único y carpeta según la predicción
        folder = "Stroke" if prediction == 1 else "Normal"
        filename = f"{folder}/{uuid4().hex}_{file.filename}"

        # Subir imagen al bucket de Supabase
        supabase.storage.from_(BUCKET_NAME).upload(filename, image_bytes)
        logging.info(f"Imagen subida a bucket de Supabase, en la carpeta '{folder}'.")

        # Insertar en base de datos
        supabase.table("img_predictions").insert({
            "filename": filename,
            "prediction": prediction,
            "probability": probability,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        logging.info(f"Registro insertado en la base de datos 'img_predictions'.")

        return {
            "filename": filename,
            "prediction": prediction,
            "probability": round(probability, 4)
        }

    except Exception as e:
        logging.error(f"Error al procesar la imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
