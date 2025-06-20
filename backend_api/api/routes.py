# /Proyecto-IX-DS2/backend_api/api/routes.py

import os
import httpx
from fastapi import APIRouter, HTTPException, status
from common.models.schemas import InputData
from ..services.storage_handler import save_prediction_results_to_db, get_predictions_from_db, clear_predictions_from_db

tabular_router = APIRouter()
history_router = APIRouter()

MODEL_SERVICE_URL = os.getenv("MODEL_API_URL", "http://localhost:8001")


# === RUTA PARA LA PREDICCIÓN TABULAR ===
# ¡¡¡CAMBIO CLAVE!!! De "/" a "". Ahora la ruta final es /predict, sin la barra.
@tabular_router.post("", tags=["Tabular Prediction"])
async def proxy_predict_tabular(data: InputData):
    """
    Recibe datos, los reenvía al servicio de modelo y guarda el resultado.
    """
    prediction_endpoint = f"{MODEL_SERVICE_URL}/infer/tabular"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(prediction_endpoint, json=data.model_dump(), timeout=60)
            response.raise_for_status()
            prediction_results = response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Servicio de modelo tabular no disponible: {e}"
        )
    
    save_prediction_results_to_db(input_data=data.model_dump(), results=prediction_results)

    return {
        "stroke": prediction_results.get("prediction"),
        "probability": f"{round(prediction_results.get('probability', 0) * 100, 2)} %"
    }

# === RUTAS PARA EL HISTORIAL (Adaptadas) ===
@history_router.get("/all-predicts", tags=["History"])
def get_all_predicts_route():
    """
    Obtiene el historial de todas las predicciones y las une para el frontend.
    """
    history_data = get_predictions_from_db()
    # Unimos ambos historiales y añadimos un campo 'type' para distinguirlos
    tabular_preds = history_data.get("tabular_predictions", [])
    for pred in tabular_preds:
        pred['type'] = 'Tabular'

    image_preds = history_data.get("image_predictions", [])
    for pred in image_preds:
        # Homogeneizamos los campos para que el frontend pueda mostrarlos igual
        pred['type'] = 'Imagen'
        pred['age'] = 'N/A' # Las predicciones de imagen no tienen edad, etc.

    # Devolvemos un único array, que es lo que el frontend probablemente espera.
    return sorted(tabular_preds + image_preds, key=lambda x: x['created_at'], reverse=True)


@history_router.delete("/clear-db", status_code=status.HTTP_204_NO_CONTENT, tags=["History"])
def clear_db_route():
    """Borra todas las predicciones de la base de datos."""
    clear_predictions_from_db()
    return