from fastapi import APIRouter
from ..services.prediction import predict_stroke
from ..services.storage import save_prediction, get_recent_predictions, clear_all_predictions
from ..models.schemas import InputData
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

router = APIRouter()

@router.post("/predict")
def predict(data: InputData):
    result = predict_stroke(data)
    save_prediction(result["input"], result["prediction"])
    return result["response"]

@router.get("/all-predicts")
def get_all_predictions():
    return JSONResponse(content=get_recent_predictions())

@router.delete("/clear-db", status_code=status.HTTP_200_OK)
def clear_predictions():
    clear_all_predictions()
    return {"message": "Predicciones eliminadas correctamente."}
