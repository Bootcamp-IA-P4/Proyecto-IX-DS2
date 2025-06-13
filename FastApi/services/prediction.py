from ..models.schemas import InputData
from ..utils.helpers import calculate_bmi, preprocess_input
from ..core.model_loader import model

def predict_stroke(data: InputData):
    data_dict = data.model_dump()
    data_dict["bmi"] = calculate_bmi(data_dict["height"], data_dict["weight"])
    input_vector = preprocess_input(data_dict)

    prediction = model.predict(input_vector).tolist()[0]
    probability = model.predict_proba(input_vector).tolist()[0][prediction]

    response = {
        "stroke": prediction,
        "probability": f"{round(probability * 100, 2)} %"
    }

    return {
        "input": data_dict,
        "prediction": prediction,
        "response": response
    }
