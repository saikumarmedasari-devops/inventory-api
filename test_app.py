
import pytest
from fastapi.testclient import TestClient

import app as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_products():
    app_module.products.clear()
    app_module.next_product_id = 1


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_product():
    response = client.post(
        "/products",
        json={"name": "Laptop", "quantity": 10},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Laptop",
        "quantity": 10,
    }


def test_list_products():
    client.post(
        "/products",
        json={"name": "Keyboard", "quantity": 5},
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_product_not_found():
    response = client.get("/products/999")

    assert response.status_code == 404


def test_negative_quantity_is_rejected():
    response = client.post(
        "/products",
        json={"name": "Mouse", "quantity": -1},
    )

    assert response.status_code == 422
