
def test_model_loaded():
    from fast_api.core.model_loader import model
    assert model is not None
    assert hasattr(model, "predict")
