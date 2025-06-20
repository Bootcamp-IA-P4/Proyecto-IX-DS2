# /backend_api/main.py

import os
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

# --- Carga de variables de entorno desde la raíz del proyecto ---
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Módulos específicos de este servicio ---
from .api.routes import tabular_router, history_router
from .services.storage_handler import save_image_results_to_db

# --- CONFIGURACIÓN DE LA APP ---
app = FastAPI(
    title="API Gateway de Predicción de Stroke",
    description="Actúa como un gateway ligero entre el frontend y los servicios de modelos.",
    version="1.0.0"
)

# --- Configuración de CORS ---
origins = ["*"]  # Para desarrollo. En producción, especifica el dominio del frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL del servicio de modelo pesado
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://localhost:8001")


# --- DEFINICIÓN DE RUTAS ---

# Ruta de bienvenida/health check
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "API Gateway está en funcionamiento."}


# Ruta de predicción de imagen (definida directamente en main.py)
@app.post("/predict-image", tags=["Image Prediction"])
async def proxy_predict_image(file: UploadFile = File(...)):
    """
    Recibe una imagen, la reenvía al servicio de modelo, guarda el resultado
    y lo devuelve al frontend.
    URL final: POST /predict-image
    """
    image_bytes = await file.read()
    files = {'file': (file.filename, image_bytes, file.content_type)}
    
    try:
        response = requests.post(f"{MODEL_SERVICE_URL}/infer/image", files=files, timeout=60)
        response.raise_for_status()
        prediction_results = response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503, 
            detail="Servicio de modelo de imágenes no disponible."
        )

    # Guarda el resultado en la BBDD después de la predicción
    save_image_results_to_db(file, image_bytes=image_bytes, results=prediction_results)
    
    return prediction_results


# === INCLUSIÓN DE LOS ROUTERS EXTERNOS ===

# Incluye el router de predicción tabular. Todas sus rutas empezarán con /predict
app.include_router(tabular_router, prefix="/predict")

# Incluye el router del historial. Como no tiene prefijo, sus rutas se usarán tal cual.
app.include_router(history_router)