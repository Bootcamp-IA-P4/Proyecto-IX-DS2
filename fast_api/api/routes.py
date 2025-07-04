from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from ..services.prediction import predict_stroke
from ..services.storage import save_prediction
from ..models.schemas import InputData

# importamos la configuración de logging
import logging
from logs.logger_setup import setup_logging
# configuramos el logger
setup_logging()

router = APIRouter()

@router.post("/predict", tags=["Prediction"])
def predict(data: InputData):
    # 1. Obtiene los datos del formulario en un diccionario.
    input_data_dict = data.model_dump()
    logging.info(f"Datos recibidos para predicción mediante formulario.")

    # 2. Llama al servicio de predicción para obtener el resultado.
    prediction_results = predict_stroke(data)
    logging.info(f"Predicción realizada, resultados obtenidos..")

    # 3. Construye el diccionario para guardar en la base de datos.
    data_to_save = input_data_dict.copy()
    
    # 4. Añadimos los resultados con los nombres de columna CORRECTOS.
    data_to_save['stroke'] = prediction_results['prediction']
    data_to_save['probability'] = prediction_results['probability']

    # 5. Pasamos este diccionario completo a la función de guardado.
    try:
        save_prediction(data_to_save)
        logging.info(f"Datos guardados correctamente en la base de datos 'predictions'.")
    except Exception as e:
        print(f"⚠️  Error al intentar guardar desde la capa de rutas: {e}")
        logging.error(f"Error al guardar los datos en la base de datos: {e}")
        
    # 6. Prepara la respuesta para el frontend
    response_for_frontend = {
        "stroke": prediction_results["prediction"],
        "probability": f"{round(prediction_results['probability'] * 100, 2)} %"
    }
    return response_for_frontend

from ..services.storage import get_recent_predictions, clear_all_predictions

@router.get("/all-predicts", tags=["History"])
def get_all_predictions():
    return JSONResponse(content=get_recent_predictions())

@router.delete("/clear-db", status_code=status.HTTP_200_OK, tags=["History"])
def clear_predictions():
    logging.warning("Eliminando todas las predicciones de la base de datos...")
    clear_all_predictions()
    logging.info("Todas las predicciones han sido eliminadas de la base de datos.")
    return {"message": "Predicciones eliminadas correctamente."}