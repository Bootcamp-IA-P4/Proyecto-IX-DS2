import requests

def test_api_up():
    try:
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        assert False, "API no está corriendo"
