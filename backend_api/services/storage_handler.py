# /Proyecto-IX-DS2/backend_api/services/storage_handler.py

import os
from supabase import create_client, Client
from uuid import uuid4
from datetime import datetime, timezone
import logging

# --- CONFIGURACIÓN DE CONEXIÓN A SUPABASE ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    logging.warning("Variables de entorno de Supabase no encontradas. Las operaciones de guardado fallarán.")
    supabase: Client = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# --- Funciones para interactuar con la BBDD ---

def save_prediction(data_to_save: dict):
    """Guarda una predicción tabular en la tabla 'predictions'."""
    if not supabase:
        logging.error("Cliente de Supabase no inicializado. No se puede guardar la predicción.")
        return

    try:
        # ==> LISTA ACTUALIZADA SEGÚN TU ESQUEMA DE SUPABASE <==
        # He copiado los nombres de las columnas exactamente de tu imagen.
        # Nota: 'id' se excluye intencionadamente porque la base de datos lo genera automáticamente.
        columnas_validas = [
            'created_at', 'gender', 'age', 'hypertension', 'heart_disease',
            'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level',
            'bmi', 'smoking_status', 'stroke', 'probability'
        ]

        # Creamos un nuevo diccionario limpio, conteniendo solo las claves válidas.
        datos_filtrados = {
            key: data_to_save[key] 
            for key in columnas_validas 
            if key in data_to_save
        }

        # Nos aseguramos de que el timestamp de creación esté presente si no viene.
        # Supabase también lo maneja con `now()`, pero esto es una buena práctica.
        if 'created_at' not in datos_filtrados:
            datos_filtrados['created_at'] = datetime.now(timezone.utc).isoformat()
        
        # Insertamos en la base de datos SÓLO los datos filtrados.
        supabase.table("predictions").insert(datos_filtrados).execute()
        logging.info("¡VICTORIA! Predicción tabular guardada exitosamente en Supabase.")

    except Exception as e:
        logging.error(f"Error al guardar predicción tabular en Supabase: {e}")

# ... (El resto del archivo no necesita cambios)

def get_predictions_from_db():
    if not supabase:
        logging.error("Cliente de Supabase no inicializado.")
        return {"error": "Conexión a la base de datos no configurada."}
    try:
        tabular_data = supabase.table("predictions").select("*").order("created_at", desc=True).execute()
        image_data = supabase.table("img_predictions").select("*").order("created_at", desc=True).execute()
        return {"tabular_predictions": tabular_data.data, "image_predictions": image_data.data}
    except Exception as e:
        logging.error(f"Error al obtener predicciones de Supabase: {e}")
        return {"error": str(e)}

def clear_predictions_from_db():
    if not supabase:
        logging.error("Cliente de Supabase no inicializado.")
        return
    try:
        supabase.table("predictions").delete().neq("id", -1).execute() 
        supabase.table("img_predictions").delete().neq("id", -1).execute()
        logging.info("Historial de predicciones borrado exitosamente.")
    except Exception as e:
        logging.error(f"Error al borrar predicciones de Supabase: {e}")

def save_prediction_results_to_db(input_data: dict, results: dict):
    data_to_save = input_data.copy()
    data_to_save['stroke'] = results.get('prediction')
    data_to_save['probability'] = results.get('probability')
    save_prediction(data_to_save)

def save_image_results_to_db(file, image_bytes: bytes, results: dict):
    if not supabase:
        logging.error("Cliente de Supabase no inicializado.")
        return
    try:
        prediction, probability = results["prediction"], results["probability"]
        folder = "Stroke" if prediction == 1 else "Normal"
        unique_filename = f"{folder}/{uuid4().hex}_{file.filename}"
        supabase.storage.from_("stroke-images").upload(unique_filename, image_bytes)
        supabase.table("img_predictions").insert({
            "filename": unique_filename, "prediction": prediction, "probability": probability,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        logging.info("Resultado de predicción de imagen guardado exitosamente.")
    except Exception as e:
        logging.error(f"Error al guardar resultado de imagen en Supabase: {e}")