
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_document_is_available() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    document = response.json()
    assert document["info"]["title"] == (
        "AI-Powered Airline Ticketing System"
    )
    assert "/health" in document["paths"]
