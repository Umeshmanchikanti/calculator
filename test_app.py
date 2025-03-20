import pytest
from app import app, calculate

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_calculate():
    assert calculate(5, 3, "add") == 8
    assert calculate(5, 3, "subtract") == 2
    assert calculate(5, 3, "multiply") == 15
    assert calculate(5, 3, "divide") == 5 / 3
    assert calculate(5, 0, "divide") == "Error! Division by zero."
    assert calculate(5, 3, "invalid") == "Invalid operation!"
    assert calculate("five", "three", "add") == "Invalid input!"

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Web Calculator" in response.data
