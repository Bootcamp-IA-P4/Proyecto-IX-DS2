# /backend_model/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Usa un import relativo para encontrar 'api' dentro del mismo paquete
from .api.routes import router as model_router 

app = FastAPI(
    title="Servicio de Modelos de Stroke",
    description="Provee endpoints para inferencia con modelos de ML (tabular y CNN).",
    version="1.0.0"
)

# Configuración de CORS
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de bienvenida/health check
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Servicio de modelos está en funcionamiento."}

# Incluye el router principal con todas las rutas de /infer/
app.include_router(model_router)