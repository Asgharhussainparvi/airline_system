from uuid import uuid4

from fastapi.testclient import TestClient


def test_airline_can_be_created(client: TestClient) -> None:
    response = client.post(
        "/airlines",
        json={"code": " pk ", "name": "Test Airline"},
    )

    assert response.status_code == 201
    airline = response.json()
    assert airline["code"] == "PK"
    assert airline["name"] == "Test Airline"
    assert airline["status"] == "active"
    assert airline["id"]


def test_duplicate_airline_code_is_rejected(
    client: TestClient,
) -> None:
    payload = {"code": "QA", "name": "First Test Airline"}

    first = client.post("/airlines", json=payload)
    second = client.post(
        "/airlines",
        json={"code": "qa", "name": "Second Test Airline"},
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_airline_list_includes_created_airline(
    client: TestClient,
) -> None:
    created = client.post(
        "/airlines",
        json={"code": "ZZ", "name": "List Test Airline"},
    )
    assert created.status_code == 201

    response = client.get("/airlines")

    assert response.status_code == 200
    assert any(
        item["id"] == created.json()["id"]
        for item in response.json()
    )


def test_airline_can_be_retrieved_by_id(
    client: TestClient,
) -> None:
    created = client.post(
        "/airlines",
        json={"code": "XY", "name": "Lookup Test Airline"},
    )
    assert created.status_code == 201

    airline_id = created.json()["id"]
    response = client.get(f"/airlines/{airline_id}")

    assert response.status_code == 200
    assert response.json()["id"] == airline_id


def test_missing_airline_returns_404(client: TestClient) -> None:
    response = client.get(f"/airlines/{uuid4()}")

    assert response.status_code == 404


def test_invalid_airline_code_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/airlines",
        json={"code": "P K", "name": "Invalid Code Airline"},
    )

    assert response.status_code == 422
