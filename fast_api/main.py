import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

script_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

from .api.routes import router as api_router

# Creamos la aplicación
app = FastAPI(title="API de Predicción de Stroke")

origins = os.getenv("FRONTEND_URLS", "").split(",")

if not all(origins):
    print("⚠️  Advertencia: No se han definido orígenes para CORS. Revisa tu archivo .env.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Bienvenido a la API modular de Predicción de Stroke!"}

app.include_router(api_router)