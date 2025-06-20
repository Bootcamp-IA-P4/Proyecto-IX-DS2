# /backend_model/api/routes.py

from fastapi import APIRouter, File, UploadFile
from common.models.schemas import InputData
from ..services.prediction import predict_stroke    # <--- ¡CAMBIO CLAVE! Con '..'
from ..core.model_logic import predict_image_data # <--- ¡CAMBIO CLAVE! Con '..'

router = APIRouter()


@router.post("/infer/tabular", tags=["Model Inference"])
def infer_tabular_route(data: InputData):
    """
    Endpoint para realizar la predicción con datos tabulares.
    """
    return predict_stroke(data)


@router.post("/infer/image", tags=["Model Inference"])
async def infer_image_route(file: UploadFile = File(...)):
    """
    Endpoint para realizar la predicción con una imagen.
    """
    image_bytes = await file.read()
    return predict_image_data(image_bytes)