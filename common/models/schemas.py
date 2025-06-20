from pydantic import BaseModel
from typing import Literal

class InputData(BaseModel):
    gender: Literal[0, 1]
    age: int
    hypertension: Literal[0, 1]
    heart_disease: Literal[0, 1]
    ever_married: Literal[0, 1]
    Residence_type: Literal[0, 1]
    avg_glucose_level: float
    height: int
    weight: int
    work_type: Literal["Govt_job", "Private", "Self-employed", "children"]
    smoking_status: Literal["Unknown", "formerly smoked", "never smoked", "smokes"]