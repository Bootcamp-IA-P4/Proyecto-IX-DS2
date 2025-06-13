import os
import csv
from dotenv import load_dotenv

load_dotenv()

# Supabase setup
supabase = None
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado a Supabase desde storage")
    except Exception as e:
        print(f"⚠️ No se pudo conectar a Supabase: {e}")
        supabase = None
else:
    print("Supabase no está configurado en storage.")

# función para guardar predicción
def save_prediction(data: dict, prediction: int):
    record = data.copy()
    record["stroke"] = prediction

    # eliminamos height y weight para no guardarlos en Supabase
    record.pop("height", None)
    record.pop("weight", None)

    if supabase:
        try:
            supabase.table("predictions").insert(record).execute()
            print("💾 Guardado en Supabase.")
        except Exception as e:
            print(f"❌ Error guardando en Supabase: {e}")
    else:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", "predictions.csv")
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)
            print("💾 Guardado localmente en data/predictions.csv")


# función para obtener últimas 10 predicciones
def get_recent_predictions(limit: int = 10):
    if supabase:
        try:
            response = (
                supabase
                .table("predictions")
                .select("*")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data if hasattr(response, "data") else response.get("data", [])
        except Exception as e:
            raise Exception(f"Error al obtener predicciones de Supabase: {str(e)}")
    else:
        file_path = os.path.join("data", "predictions.csv")
        if not os.path.exists(file_path):
            return []

        with open(file_path, mode="r") as file:
            reader = list(csv.DictReader(file))
            return reader[-limit:] if reader else []

# función para limpiar la base de datos
def clear_all_predictions():
    if supabase:
        try:
            supabase.table("predictions").delete().neq("id", 0).execute()
            print("🧹 Supabase limpiado correctamente.")
        except Exception as e:
            raise Exception(f"Error al limpiar Supabase: {str(e)}")
    else:
        file_path = os.path.join("data", "predictions.csv")
        if os.path.exists(file_path):
            os.remove(file_path)
            print("🧹 Archivo local predictions.csv eliminado.")
