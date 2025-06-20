import os
import csv

# Configuración del logger
import logging
from logs.logger_setup import setup_logging
setup_logging()

supabase = None
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("Conectado a Supabase desde storage.")
        print("✅ Conectado a Supabase desde storage")
    except Exception as e:
        logging.error(f"No se pudo conectar a Supabase desde storage: {e}")
        print(f"⚠️ No se pudo conectar a Supabase desde storage: {e}")
        supabase = None
else:
    logging.warning("Variables de Supabase no encontradas.")
    print("Variables de Supabase no encontradas.")

def save_prediction(data_to_save: dict):
    """
    Recibe un diccionario COMPLETO y lo limpia ANTES de guardarlo.
    """
    # Crea una copia para trabajar de forma segura.
    record_to_save = data_to_save.copy()
    
    # Elimina las claves que NO existen en la tabla de Supabase.
    record_to_save.pop('height', None)
    record_to_save.pop('weight', None)
    
    # Inserta el diccionario ya limpio.
    if supabase:
        try:
            supabase.table("predictions").insert(record_to_save).execute()
            logging.info("Datos guardados en Supabase correctamente.")
            print("💾 ¡Éxito! Datos guardados en Supabase.")
        except Exception as e:
            logging.error(f"Error guardando en Supabase: {e}")
            print(f"❌ Error guardando en Supabase: {e}")


def get_recent_predictions(limit: int = 10):
    if supabase:
        try:
            response = (
                supabase.table("predictions").select("*").order("created_at", desc=True).limit(limit).execute()
            )
            logging.info(f"Predicciones obtenidas de Supabase.")
            return response.data if hasattr(response, "data") and response.data else []
        except Exception as e:
            logging.error(f"Error al obtener predicciones de Supabase: {e}")
            print(f"❌ Error al obtener predicciones de Supabase: {e}")
            return []
    return []

def clear_all_predictions():
    if supabase:
        try:
            supabase.table("predictions").delete().neq("id", 0).execute()
            print("🧹 Supabase limpiado correctamente.")
        except Exception as e:
            print(f"❌ Error al limpiar Supabase: {e}")