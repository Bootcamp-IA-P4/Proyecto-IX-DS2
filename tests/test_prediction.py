from fast_api.models.schemas import InputData
from fast_api.services.prediction import predict_stroke
from fast_api.services.prediction import preprocess_input

def test_predict_valid_result():
    data = InputData(
        gender=1,
        age=55,
        hypertension=1,
        heart_disease=0,
        ever_married=1,
        Residence_type=1,
        avg_glucose_level=105.0,
        height=170,
        weight=70,
        work_type="Private",
        smoking_status="never smoked"
    )

    result = predict_stroke(data)

    assert isinstance(result, dict)
    assert "prediction" in result
    assert "probability" in result
    assert result["prediction"] in [0, 1]
    assert result["probability"] >= 0.0 and result["probability"] <= 1.0


def test_preprocess_input_correctly():
    input_data = {
        "gender": 1,
        "age": 55,
        "hypertension": 1,
        "heart_disease": 0,
        "ever_married": 1,
        "Residence_type": 1,
        "avg_glucose_level": 105.0,
        "height": 170,
        "weight": 70,
        "work_type": "Private",
        "smoking_status": "never smoked"
    }

    df = preprocess_input(input_data)
    assert "bmi" in df.columns
    assert "height" not in df.columns
    assert "weight" not in df.columns