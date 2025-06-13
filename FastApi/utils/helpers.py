def calculate_bmi(height: int, weight: int) -> float:
    if height <= 0 or weight <= 0:
        raise ValueError("Altura y peso deben ser mayores que cero.")
    return round(weight / ((height / 100) ** 2), 2)

import pandas as pd

WORK_TYPE_OPTIONS = ["Govt_job", "Private", "Self-employed", "children"]
SMOKING_STATUS_OPTIONS = ["Unknown", "formerly smoked", "never smoked", "smokes"]

def preprocess_input(data: dict):
    columns = [
        "gender", "age", "hypertension", "heart_disease", "ever_married",
        "Residence_type", "avg_glucose_level", "bmi",
        "work_type_Govt_job", "work_type_Private", "work_type_Self-employed", "work_type_children",
        "smoking_status_Unknown", "smoking_status_formerly smoked", "smoking_status_never smoked", "smoking_status_smokes"
    ]
    features = [
        data["gender"], data["age"], data["hypertension"], data["heart_disease"],
        data["ever_married"], data["Residence_type"], data["avg_glucose_level"], data["bmi"]
    ]
    work_type_vector = [1 if data["work_type"] == opt else 0 for opt in WORK_TYPE_OPTIONS]
    smoking_vector = [1 if data["smoking_status"] == opt else 0 for opt in SMOKING_STATUS_OPTIONS]
    return pd.DataFrame([features + work_type_vector + smoking_vector], columns=columns)
