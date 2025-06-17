import pandas as pd
from ..models.schemas import InputData
from ..core.model_loader import load_joblib_model
from ..utils.helpers import WORK_TYPE_OPTIONS, SMOKING_STATUS_OPTIONS

# Configuración del logger
import logging
from logs.logger_setup import setup_logging
setup_logging()

model = load_joblib_model()

def preprocess_input(data: dict):
    height_m = data["height"] / 100
    bmi = data["weight"] / (height_m * height_m) if height_m > 0 else 0
    logging.info(f"BMI calculado correctamente.")

    features = [
        data["gender"], data["age"], data["hypertension"], data["heart_disease"],
        data["ever_married"], data["Residence_type"], data["avg_glucose_level"], bmi
    ]
    
    columns = [
        "gender", "age", "hypertension", "heart_disease", "ever_married", "Residence_type", 
        "avg_glucose_level", "bmi", "work_type_Govt_job", "work_type_Private", 
        "work_type_Self-employed", "work_type_children", "smoking_status_Unknown", 
        "smoking_status_formerly smoked", "smoking_status_never smoked", "smoking_status_smokes"
    ]
    work_type_vector = [1 if data["work_type"] == option else 0 for option in WORK_TYPE_OPTIONS]
    smoking_vector = [1 if data["smoking_status"] == option else 0 for option in SMOKING_STATUS_OPTIONS]
    arr = features + work_type_vector + smoking_vector
    df = pd.DataFrame([arr], columns=columns)
    logging.info(f"Datos de entrada preprocesados correctamente.")
    return df

def predict_stroke(data: InputData):
    """
    Realiza la predicción y devuelve ÚNICAMENTE los resultados.
    """
    try:
        data_dict = data.model_dump()
        logging.info(f"Datos recibidos.")
        input_vector = preprocess_input(data_dict)
        logging.info(f"Vector de entrada preprocesado.")
        
        prediction_result = model.predict(input_vector)[0]
        logging.info(f"Predicción realizada: {prediction_result}.")
        probabilities = model.predict_proba(input_vector)[0]
        probability_result = probabilities[prediction_result]
        logging.info(f"Probabilidad calculada: {probabilities}.")

        
        return {
            "prediction": int(prediction_result),
            "probability": float(probability_result)
        }
        
    except Exception as e:
        logging.error(f"Error en el servicio de predicción: {e}")
        print(f"❌ Error en el servicio de predicción: {e}")
        raise e