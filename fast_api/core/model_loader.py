import os, joblib
model_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "model.pkl")
model = joblib.load(model_path)
