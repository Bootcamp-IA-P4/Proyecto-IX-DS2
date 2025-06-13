from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

model_path = os.path.join(os.path.dirname(__file__), "..", "data", "model.pkl")

# cargamos las variables de entorno
load_dotenv()

# iniciamos Supabase si existen las variables de entorno
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
    print("Supabase no está configurado. Ejecutando solo en local.")

# cargamos el modelo
try:
    model = joblib.load(model_path)
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    raise RuntimeError(f"❌ Error cargando el modelo: {e}")

# creamos la app FastAPI
app = FastAPI(title="API de Predicción de Stroke")

# creamos las opciones de work_type y smoking_status
WORK_TYPE_OPTIONS = ["Govt_job", "Private", "Self-employed", "children"]
SMOKING_STATUS_OPTIONS = ["Unknown", "formerly smoked", "never smoked", "smokes"]

# declaramos las variables de input
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

# preprocesamos los datos para que coincidan con el modelo
import pandas as pd
def preprocess_input(data: dict):
    columns = [
        "gender", "age", "hypertension", "heart_disease", "ever_married",
        "Residence_type", "avg_glucose_level", "bmi",
        "work_type_Govt_job", "work_type_Private", "work_type_Self-employed", "work_type_children",
        "smoking_status_Unknown", "smoking_status_formerly smoked", "smoking_status_never smoked", "smoking_status_smokes"
    ]
    features = [
        data["gender"],
        data["age"],
        data["hypertension"],
        data["heart_disease"],
        data["ever_married"],
        data["Residence_type"],
        data["avg_glucose_level"],
        data["bmi"],
    ]
    work_type_vector = [1 if data["work_type"] == option else 0 for option in WORK_TYPE_OPTIONS]
    smoking_vector = [1 if data["smoking_status"] == option else 0 for option in SMOKING_STATUS_OPTIONS]

    # DataFrame con columnas y datos
    arr = features + work_type_vector + smoking_vector
    df = pd.DataFrame([arr], columns=columns)
    return df

# endpoint de predicción
@app.post("/predict")
def predict(data: InputData):
    try:
        data_dict = data.model_dump()
        print("📥 Datos recibidos:", data_dict)
        input_vector = preprocess_input(data_dict)
        print("📊 Vector transformado:", input_vector)
        prediction = model.predict(input_vector).tolist()[0]
        probability = model.predict_proba(input_vector).tolist()[0][prediction]
        print("✅ Predicción:", prediction)
        print("📈 Probabilidad:", f"{round(probability * 100)} %")

        # guardamos en Supabase si la conexión está activa
        if supabase:
            supabase.table("predictions").insert({
                **data_dict,
                "stroke": prediction
            }).execute()

        return {
            "stroke": prediction,
            "probability": f"{round(probability * 100, 2)} %"
        }

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

# endpoint para obtener las últimas 10 predicciones
@app.get("/all-predicts")
def get_all_predictions():
    if not supabase:
        raise HTTPException(status_code=503, detail="Supabase no está conectado.")
    try:
        response = (
            supabase
            .table("predictions")
            .select("*")
            .order("created_at", desc=True)
            .limit(10)
            .execute()
        )
        data = response.data if hasattr(response, "data") else response.get("data", [])
        return JSONResponse(content=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")


# endpoint para limpiar la base de datos
@app.delete("/clear-db", status_code=status.HTTP_200_OK)
def clear_predictions():
    try:
        if supabase:
            response = supabase.table("predictions").delete().neq("id", 0).execute()
            print("🧹 Base de datos vaciada.")
            return {"message": "Predicciones eliminadas correctamente."}
        else:
            raise HTTPException(status_code=503, detail="Supabase no está configurado.")
    except Exception as e:
        print("❌ Error al vaciar la base de datos:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al vaciar la base de datos: {str(e)}")
