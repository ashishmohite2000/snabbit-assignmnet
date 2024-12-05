from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_dynamic_pricing():
    response = client.get("/pricing/1?location=NY&time_of_day=peak")
    assert response.status_code == 200
    assert "price" in response.json()
    assert response.json()["product"] == "Test Product"
