# /backend_model/services/prediction.py

import pandas as pd
import logging
import traceback
from common.models.schemas import InputData
from ..core.model_loader import load_joblib_model

# Configuración de logging
logger = logging.getLogger(__name__)

# --- CARGA DEL MODELO ---
# Tal como dijiste, solo el model.pkl, que probablemente es un Pipeline
# o un modelo que espera datos ya pre-procesados.
model = load_joblib_model()

# --- CONSTANTES DE PRE-PROCESAMIENTO ---
# Mapeos para el Label Encoding
GENDER_MAP = {"Male": 1, "Female": 0, "Other": 2}
MARRIED_MAP = {"Yes": 1, "No": 0}
RESIDENCE_MAP = {"Urban": 1, "Rural": 0}

# ¡LA LISTA DE LA VERDAD! Esta es la lista que usaremos para forzar el orden.
# Debe ser la que sacaste de X_train.columns.tolist() en tu notebook.
TRAINING_COLUMNS_ORDER = [ 
    'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'Residence_type',
    'avg_glucose_level', 'bmi', 'work_type_Govt_job', 'work_type_Private',
    'work_type_Self-employed', 'work_type_children', 'smoking_status_Unknown',
    'smoking_status_formerly smoked', 'smoking_status_never smoked', 'smoking_status_smokes'
]


def preprocess_for_prediction(data_dict: dict) -> pd.DataFrame:
    """
    Aplica el pre-procesamiento sin scaler externo.
    """
    df = pd.DataFrame([data_dict])
    
    # 1. BMI: Cálculo e imputación
    if data_dict.get('height') and data_dict.get('weight'):
        height_m = data_dict['height'] / 100
        df['bmi'] = data_dict['weight'] / (height_m * height_m) if height_m > 0 else 0
    else:
        # Usa el mismo valor de imputación que en tu entrenamiento.
        # ¿Estás seguro de que era 28.89? Vamos a usarlo por ahora.
        df['bmi'] = 28.89 
    
    df = df.drop(columns=['height', 'weight'], errors='ignore')

    # 2. Label Encoding
    df['gender'] = df['gender'].map(GENDER_MAP)
    df['ever_married'] = df['ever_married'].map(MARRIED_MAP)
    df['Residence_type'] = df['Residence_type'].map(RESIDENCE_MAP)
    
    # 3. One-Hot Encoding
    cols_to_one_hot = ['work_type', 'smoking_status']
    df = pd.get_dummies(df, columns=cols_to_one_hot, dtype=int)
    
    # 4. Alinear y Ordenar Columnas
    # Añade las columnas que falten
    for col in TRAINING_COLUMNS_ORDER:
        if col not in df.columns:
            df[col] = 0
            
    # Asegura el orden final
    return df[TRAINING_COLUMNS_ORDER]


def predict_stroke(data: InputData):
    """
    Punto de entrada principal para la predicción tabular.
    """
    try:
        data_dict = data.model_dump()
        processed_df = preprocess_for_prediction(data_dict)
        
        # === DEPURACIÓN CLAVE: MUESTRA EL DATAFRAME EXACTO ===
        print("--- DataFrame que entra al modelo .predict() ---")
        print(processed_df.to_string())
        print("---------------------------------------------")
        
        prediction_result = model.predict(processed_df)[0]
        probabilities = model.predict_proba(processed_df)[0]
        probability_of_stroke = probabilities[1] 

        return {
            "prediction": int(prediction_result),
            "probability": float(probability_of_stroke)
        }
        
    except Exception as e:
        logger.error(f"Error crítico en el servicio de predicción: {e}", exc_info=True)
        traceback.print_exc()
        raise e