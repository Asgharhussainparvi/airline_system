
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customer_routes_are_registered() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]

    assert "/customers" in paths
    assert "get" in paths["/customers"]
    assert "post" in paths["/customers"]


def test_customer_create_schema_rejects_missing_display_name() -> None:
    response = client.post(
        "/customers",
        json={"email": "customer@example.test"},
    )

    assert response.status_code == 422


def test_customer_create_rejects_invalid_status() -> None:
    response = client.post(
        "/customers",
        json={"display_name": "Test Customer", "status": "deleted"},
    )

    assert response.status_code == 422


def test_customer_create_rejects_blank_display_name() -> None:
    response = client.post(
        "/customers",
        json={"display_name": "   "},
    )

    assert response.status_code == 422


def test_customer_create_rejects_invalid_email() -> None:
    response = client.post(
        "/customers",
        json={"display_name": "Test Customer", "email": "not-an-email"},
    )

    assert response.status_code == 422
