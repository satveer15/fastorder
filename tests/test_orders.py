import pytest
from fastapi import status


@pytest.fixture
def auth_token(client, test_user):
    """Get auth token for test user"""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Get authorization headers"""
    return {"Authorization": f"Bearer {auth_token}"}


def test_create_order(client, auth_headers):
    """Test creating an order"""
    response = client.post(
        "/orders/",
        headers=auth_headers,
        json={
            "item_name": "Test Item",
            "quantity": 2,
            "price": 29.99
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["item_name"] == "Test Item"
    assert data["quantity"] == 2
    assert data["status"] == "pending"


def test_get_my_orders(client, auth_headers):
    """Test getting user's orders"""
    # Create an order first
    client.post(
        "/orders/",
        headers=auth_headers,
        json={"item_name": "Item 1", "quantity": 1, "price": 10.0}
    )

    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1


def test_get_order_by_id(client, auth_headers):
    """Test getting a specific order"""
    # Create order
    create_response = client.post(
        "/orders/",
        headers=auth_headers,
        json={"item_name": "Item", "quantity": 1, "price": 15.0}
    )
    order_id = create_response.json()["id"]

    # Get order
    response = client.get(f"/orders/{order_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == order_id


def test_unauthorized_access(client):
    """Test accessing orders without auth"""
    response = client.get("/orders/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_cancel_order(client, auth_headers):
    """Test cancelling an order"""
    # Create order
    create_response = client.post(
        "/orders/",
        headers=auth_headers,
        json={"item_name": "Item", "quantity": 1, "price": 20.0}
    )
    order_id = create_response.json()["id"]

    # Cancel order
    response = client.delete(f"/orders/{order_id}/cancel", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "cancelled"
