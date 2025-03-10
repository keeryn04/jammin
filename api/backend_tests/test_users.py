import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask
import pytest
from unittest import mock
from api.database_connector import get_db_connection
from api.routes.users import user_routes

@pytest.fixture
def mock_db_connection():
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

@pytest.fixture
def test_client():
    app = Flask(__name__)  
    app.register_blueprint(user_routes)
    client = app.test_client()
    return client

def test_get_db_connection(mock_db_connection, mocker):
    mocker.patch('api.database_connector.get_db_connection', return_value=mock_db_connection)
    conn = get_db_connection()
    assert conn == mock_db_connection

def test_get_users(mock_db_connection, mocker, test_client):
    #Mocking, return fake data
    mock_cursor = mock_db_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {"match_id": "1", "user_1_id": "user1", "user_2_id": "user2", "match_score": "10-8", "status": "ongoing"},
        {"match_id": "2", "user_1_id": "user3", "user_2_id": "user4", "match_score": "5-3", "status": "completed"}
    ]
    
    #Mocking the Flask route
    mocker.patch('api.database_connector.get_db_connection', return_value=mock_db_connection)

    response = test_client.get('/api/users')
        
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["match_id"] == "1"