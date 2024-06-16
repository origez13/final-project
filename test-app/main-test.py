import os
import sys
import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection import app  # Import the FastAPI app from main.py

# Define the MongoDB URI for testing
TEST_MONGO_URI = 'mongodb://localhost:27017/'  # Update URI to use Docker service name


@pytest.fixture
def client():
    # Set up the FastAPI TestClient
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Set up the MongoDB test database connection
    client = MongoClient(TEST_MONGO_URI)
    db = client.get_database()
    users_collection = db.mycollection

    # Clean up the test database before and after each test
    yield
    users_collection.delete_many({})


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200  # Ensure it responds with OK
