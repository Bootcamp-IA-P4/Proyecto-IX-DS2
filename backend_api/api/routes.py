# /backend_api/api/routes.py

import os
import requests
from fastapi import APIRouter, HTTPException, status
from common.models.schemas import InputData
# Se asume que get_recent_predictions y clear_all_predictions funcionan llamando a una BBDD
# compartida o a través de otro servicio si es necesario.
from backend_model.services.storage import get_recent_predictions, clear_all_predictions 
from ..services.storage_handler import save_prediction_results_to_db

# --- CREAMOS LOS DOS ROUTERS ---
tabular_router = APIRouter()
history_router = APIRouter()

# URL del servicio pesado, leída desde las variables de entorno
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://localhost:8001")


# === RUTA PARA LA PREDICCIÓN TABULAR ===
@tabular_router.post("/", tags=["Tabular Prediction"]) # <--- ¡CAMBIO CLAVE! De "/predict" a "/"
def proxy_predict_tabular(data: InputData):
    """
    Recibe los datos del formulario, los reenvía al servicio de modelo pesado
    y guarda el resultado antes de devolverlo al frontend.
    URL final será: POST /predict
    """
    try:
        # Llama al endpoint /infer/tabular del servicio de modelo
        response = requests.post(f"{MODEL_SERVICE_URL}/infer/tabular", json=data.model_dump())
        response.raise_for_status()  # Lanza una excepción para respuestas de error (4xx/5xx)
        prediction_results = response.json()
    except requests.RequestException as e:
        # Esto captura errores de conexión, timeouts, etc.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Servicio de modelo tabular no disponible: {e}"
        )
    
    # Después de una predicción exitosa, guarda los resultados
    save_prediction_results_to_db(input_data=data.model_dump(), results=prediction_results)

    # Devuelve el resultado formateado al frontend
    return {
        "stroke": prediction_results.get("prediction"),
        "probability": f"{round(prediction_results.get('probability', 0) * 100, 2)} %"
    }


# === RUTAS PARA EL HISTORIAL ===
@history_router.get("/all-predicts", tags=["History"])
def get_all_predicts_route():
    """
    Obtiene el historial de todas las predicciones.
    URL final será: GET /all-predicts
    """
    return get_recent_predictions()

@history_router.delete("/clear-db", status_code=status.HTTP_204_NO_CONTENT, tags=["History"])
def clear_db_route():
    """
    Borra todas las predicciones de la base de datos.
    URL final será: DELETE /clear-db
    """
    clear_all_predictions()
    # No es necesario devolver un mensaje en un 204
    return