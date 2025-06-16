import os
import io
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import torch
from torchvision import transforms
from supabase import create_client
from dotenv import load_dotenv

from fast_api.models.schemas import SimpleCNN

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET_NAME = "stroke-images"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

img_router = APIRouter()

# Modelo PyTorch
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../data/cnn_pytorch.pth")
model = SimpleCNN(num_classes=2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

IMG_SIZE = 224

# Transformación para las imágenes
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

@img_router.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Formato de imagen no válido.")

    try:
        # Leer y transformar la imagen
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)

        # Predicción
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            prediction = int(torch.argmax(probabilities, dim=1).item())
            probability = float(probabilities[0][prediction].item())

        # Nombre de archivo único y carpeta según la predicción
        folder = "Stroke" if prediction == 1 else "Normal"
        filename = f"{folder}/{uuid4().hex}_{file.filename}"

        # Subir imagen al bucket de Supabase
        supabase.storage.from_(BUCKET_NAME).upload(filename, image_bytes)

        # Insertar en base de datos
        supabase.table("img_predictions").insert({
            "filename": filename,
            "prediction": prediction,
            "probability": probability,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()

        return {
            "filename": filename,
            "prediction": prediction,
            "probability": round(probability, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
