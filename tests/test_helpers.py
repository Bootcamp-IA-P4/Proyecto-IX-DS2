import pytest
from fast_api.utils.helpers import calculate_bmi

def test_calculate_bmi_valid():
    assert calculate_bmi(180, 80) == 24.69

def test_bmi_zero_height():
    with pytest.raises(ValueError):
        calculate_bmi(0, 80)

def test_bmi_negative_weight():
    with pytest.raises(ValueError):
        calculate_bmi(180, -10)
