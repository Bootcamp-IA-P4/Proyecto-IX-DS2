import os
import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- Carga de variables de entorno desde el .env raíz ---
# Esto asegura que siempre se carguen, sin importar desde dónde se ejecute el script.
load_dotenv() 

# --- Módulos específicos de este servicio ---
from .api.routes import tabular_router, history_router
from .services.storage_handler import save_image_results_to_db

# --- CONFIGURACIÓN DE LA APP ---
app = FastAPI(
    title="API Gateway de Predicción de Stroke",
    version="1.0.0"
)

# --- Configuración de CORS ---
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL del servicio de modelo pesado, leída de las variables de entorno
MODEL_SERVICE_URL = os.getenv("MODEL_API_URL", "http://localhost:8001")

# --- DEFINICIÓN DE RUTAS ---

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "API Gateway está en funcionamiento."}

@app.post("/predict-image", tags=["Image Prediction"])
async def proxy_predict_image(file: UploadFile = File(...)):
    """
    Recibe una imagen, la reenvía al servicio de modelo y guarda el resultado.
    """
    image_bytes = await file.read()
    files = {'file': (file.filename, image_bytes, file.content_type)}
    prediction_endpoint = f"{MODEL_SERVICE_URL}/infer/image"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(prediction_endpoint, files=files, timeout=60)
            response.raise_for_status()
            prediction_results = response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Servicio de modelo de imágenes no disponible: {e}"
        )

    save_image_results_to_db(file, image_bytes=image_bytes, results=prediction_results)
    
    return prediction_results

# === INCLUSIÓN DE ROUTERS ===
app.include_router(tabular_router, prefix="/predict")
app.include_router(history_router)