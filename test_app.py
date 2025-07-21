import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "addition-service"}

def test_addition_success():
    """Test successful addition operation."""
    response = client.get("/?first_number=5&second_number=3")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 8.0
    assert data["operation"] == "addition"
    assert data["first_number"] == 5.0
    assert data["second_number"] == 3.0

def test_addition_with_decimals():
    """Test addition with decimal numbers."""
    response = client.get("/?first_number=7.5&second_number=2.5")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 10.0

def test_addition_negative_numbers():
    """Test addition with negative numbers."""
    response = client.get("/?first_number=-10&second_number=5")
    assert response.status_code == 200
    assert response.json()["result"] == -5.0

def test_addition_default_values():
    """Test addition with default values (0+0)."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["result"] == 0.0

def test_addition_large_numbers():
    """Test addition with large numbers."""
    response = client.get("/?first_number=1000000&second_number=2000000")
    assert response.status_code == 200
    assert response.json()["result"] == 3000000.0