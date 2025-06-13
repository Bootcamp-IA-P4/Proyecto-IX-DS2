import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- CAMBIO CLAVE 1: Cargar la configuración aquí, al inicio de todo ---
# Esto asegura que las variables de entorno estén disponibles para toda la app.
script_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path)

# Importamos las rutas DESPUÉS de cargar el .env
from .api.routes import router as api_router

# Creamos la aplicación
app = FastAPI(title="API de Predicción de Stroke")

# --- CAMBIO CLAVE 2: Configurar CORS ---
# Leemos los orígenes permitidos desde el .env que ya cargamos
origins = os.getenv("FRONTEND_URLS", "").split(",")

if not all(origins):
    print("⚠️  Advertencia: No se han definido orígenes para CORS. Revisa tu archivo .env.")

# Añadimos el middleware de CORS a la aplicación.
# ¡IMPORTANTE! Esto debe hacerse ANTES de incluir los routers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir GET, POST, DELETE, etc.
    allow_headers=["*"],
)

# --- CAMBIO CLAVE 3: Añadir un endpoint raíz para tests ---
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Bienvenido a la API modular de Predicción de Stroke!"}

# Finalmente, incluimos las rutas de nuestra API
app.include_router(api_router)