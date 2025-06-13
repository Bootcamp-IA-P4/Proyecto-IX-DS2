from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI(title="API de Predicción de Stroke")
app.include_router(api_router)
