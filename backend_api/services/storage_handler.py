# /backend_api/services/storage_handler.py
from backend_model.services.storage import save_prediction
from uuid import uuid4
from datetime import datetime, timezone
from backend_model.services.storage import supabase
import logging

def save_prediction_results_to_db(input_data: dict, results: dict):
    """Combina datos de entrada y resultados para guardarlos."""
    data_to_save = input_data.copy()
    data_to_save['stroke'] = results['prediction']
    data_to_save['probability'] = results['probability']
    save_prediction(data_to_save)

def save_image_results_to_db(file, image_bytes: bytes, results: dict):
    """Sube imagen y guarda el registro de predicción de imagen."""
    try:
        prediction = results["prediction"]
        probability = results["probability"]
        folder = "Stroke" if prediction == 1 else "Normal"
        unique_filename = f"{folder}/{uuid4().hex}_{file.filename}"

        supabase.storage.from_("stroke-images").upload(unique_filename, image_bytes)
        
        supabase.table("img_predictions").insert({
            "filename": unique_filename,
            "prediction": prediction,
            "probability": probability,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
    except Exception as e:
        logging.error(f"Error al guardar resultado de imagen en Supabase: {e}")