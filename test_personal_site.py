import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Idris Fagbemi' in response.data

def test_calendly(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Schedule time with me' in response.data
