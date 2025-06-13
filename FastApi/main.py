from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# --- CAMBIO CLAVE 1: Ruta explícita al archivo .env ---
# Obtenemos la ruta al directorio donde se encuentra este script (main.py)
script_dir = os.path.dirname(__file__)
# Construimos la ruta completa al archivo .env
dotenv_path = os.path.join(script_dir, '.env')
# Cargamos las variables de entorno desde esa ruta específica
load_dotenv(dotenv_path=dotenv_path)

# --- El resto del código de configuración de CORS ---
frontend_urls = os.getenv("FRONTEND_URLS", "")
origins = [url.strip() for url in frontend_urls.split(",") if url.strip()]

if not origins:
    print("⚠️  Advertencia: No se han definido orígenes para CORS en la variable de entorno FRONTEND_URLS. (Asegúrese de que el archivo .env está en la carpeta FastApi)")

app = FastAPI(title="API de Predicción de Stroke")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CAMBIO CLAVE 2: Añadir un endpoint raíz ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bienvenido a la API de Predicción de Stroke!"}

# --- A partir de aquí, tu código sigue igual ---

model_path = os.path.join(os.path.dirname(__file__), "..", "data", "model.pkl")

supabase = None
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado a Supabase")
    except Exception as e:
        print(f"⚠️ No se pudo conectar a Supabase: {e}")
        supabase = None
else:
    print("ℹ️ Supabase no está configurado. Ejecutando solo en local.")

try:
    model = joblib.load(model_path)
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    raise RuntimeError(f"❌ Error cargando el modelo: {e}")

WORK_TYPE_OPTIONS = ["Govt_job", "Private", "Self-employed", "children"]
SMOKING_STATUS_OPTIONS = ["Unknown", "formerly smoked", "never smoked", "smokes"]

class InputData(BaseModel):
    gender: Literal[0, 1]
    age: int
    hypertension: Literal[0, 1]
    heart_disease: Literal[0, 1]
    ever_married: Literal[0, 1]
    Residence_type: Literal[0, 1]
    avg_glucose_level: float
    bmi: float
    work_type: Literal["Govt_job", "Private", "Self-employed", "children"]
    smoking_status: Literal["Unknown", "formerly smoked", "never smoked", "smokes"]

import pandas as pd
def preprocess_input(data: dict):
    columns = [ "gender", "age", "hypertension", "heart_disease", "ever_married", "Residence_type", "avg_glucose_level", "bmi", "work_type_Govt_job", "work_type_Private", "work_type_Self-employed", "work_type_children", "smoking_status_Unknown", "smoking_status_formerly smoked", "smoking_status_never smoked", "smoking_status_smokes" ]
    features = [ data["gender"], data["age"], data["hypertension"], data["heart_disease"], data["ever_married"], data["Residence_type"], data["avg_glucose_level"], data["bmi"], ]
    work_type_vector = [1 if data["work_type"] == option else 0 for option in WORK_TYPE_OPTIONS]
    smoking_vector = [1 if data["smoking_status"] == option else 0 for option in SMOKING_STATUS_OPTIONS]
    arr = features + work_type_vector + smoking_vector
    df = pd.DataFrame([arr], columns=columns)
    return df

@app.post("/predict")
def predict(data: InputData):
    try:
        data_dict = data.model_dump()
        input_vector = preprocess_input(data_dict)
        prediction = model.predict(input_vector).tolist()[0]
        probability = model.predict_proba(input_vector).tolist()[0][prediction]
        if supabase:
            supabase.table("predictions").insert({ "input": data_dict, "stroke": prediction, "probability": probability }).execute()
        return { "stroke": prediction, "probability": f"{round(probability * 100, 2)} %" }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

@app.get("/all-predicts")
def get_all_predictions():
    if not supabase:
        raise HTTPException(status_code=503, detail="Supabase no está conectado. Revisa las variables de entorno.")
    try:
        response = ( supabase.table("predictions").select("*").order("created_at", desc=True).limit(10).execute() )
        data = response.data if hasattr(response, "data") else response.get("data", [])
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")