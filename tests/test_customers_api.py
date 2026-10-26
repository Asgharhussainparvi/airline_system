from fastapi.testclient import TestClient


def test_customer_routes_are_registered(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]

    assert "/customers" in paths
    assert "get" in paths["/customers"]
    assert "post" in paths["/customers"]


def test_customer_create_schema_rejects_missing_display_name(
    client: TestClient,
) -> None:
    response = client.post(
        "/customers",
        json={"email": "customer@example.test"},
    )

    assert response.status_code == 422


def test_customer_create_rejects_invalid_status(
    client: TestClient,
) -> None:
    response = client.post(
        "/customers",
        json={"display_name": "Test Customer", "status": "deleted"},
    )

    assert response.status_code == 422


def test_customer_create_rejects_blank_display_name(
    client: TestClient,
) -> None:
    response = client.post(
        "/customers",
        json={"display_name": "   "},
    )

    assert response.status_code == 422


def test_customer_create_rejects_invalid_email(
    client: TestClient,
) -> None:
    response = client.post(
        "/customers",
        json={"display_name": "Test Customer", "email": "not-an-email"},
    )

    assert response.status_code == 422


def test_customer_can_be_created(client: TestClient) -> None:
    payload = {
        "display_name": "Integration Test Customer",
        "email": "integration-test@example.com",
        "phone": "+923001234567",
    }

    response = client.post("/customers", json=payload)

    assert response.status_code == 201

    customer = response.json()
    assert customer["display_name"] == payload["display_name"]
    assert customer["email"] == payload["email"]
    assert customer["phone"] == payload["phone"]
    assert customer["status"] == "active"
    assert customer["id"]
    assert customer["created_at"]


def test_created_customer_appears_in_customer_list(
    client: TestClient,
) -> None:
    payload = {
        "display_name": "List Verification Customer",
        "email": "list-verification@example.com",
    }

    create_response = client.post("/customers", json=payload)
    assert create_response.status_code == 201

    customer_id = create_response.json()["id"]

    list_response = client.get("/customers")

    assert list_response.status_code == 200
    customers = list_response.json()

    matching_customers = [
        customer for customer in customers
        if customer["id"] == customer_id
    ]

    assert len(matching_customers) == 1
    assert matching_customers[0]["display_name"] == payload["display_name"]


