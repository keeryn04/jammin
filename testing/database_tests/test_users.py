import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.routes.users import user_routes

class TestUsersRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(user_routes)
        self.client = self.app.test_client()

    @patch('api.routes.users.get_db_connection')
    def test_get_users_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.return_value = MagicMock(data=[{"id": 1, "name": "Test User"}])
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": 1, "name": "Test User"}])

    @patch('api.routes.users.get_db_connection')
    def test_get_users_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

    @patch('api.routes.users.get_db_connection')
    def test_get_user_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"id": 1, "name": "Test User"}])
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/users/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"id": 1, "name": "Test User"}])

    @patch('api.routes.users.get_db_connection')
    def test_get_user_invalid_id(self, mock_get_db_connection):
        response = self.client.get('/api/users/invalid-uuid')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user_id format", response.json["error"])

    @patch('api.routes.users.get_db_connection')
    def test_add_user_success(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_conn.table.return_value.insert.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"user_data_id": "mock_user_data_id"}])
        mock_get_db_connection.return_value = mock_conn

        # Define the user data to be sent in the request
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "age": 25,
            "gender": "male",
            "spotify_auth": False,
            "bio": "This is a test bio"
        }

        # Send a POST request to the /api/users endpoint
        response = self.client.post('/api/users', json=user_data)

        # Assert the response status code and message
        self.assertEqual(response.status_code, 201)
        self.assertIn("Register successful", response.json["message"])

        # Verify that the database inserts were called
        mock_conn.table.assert_any_call("users_music_data")
        mock_conn.table.assert_any_call("users")

    @patch('api.routes.users.get_db_connection')
    def test_update_user_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_get_db_connection.return_value = mock_conn

        user_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password_hash": "new_hashed_password",
            "age": 30,
            "gender": "female"
        }
        response = self.client.put('/api/users/123e4567-e89b-12d3-a456-426614174000', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User updated successfully", response.json["message"])

    @patch('api.routes.users.get_db_connection')
    def test_delete_user_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_get_db_connection.return_value = mock_conn

        response = self.client.delete('/api/users/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", response.json["message"])

    @patch('api.routes.users.get_db_connection')
    def test_get_user_id_by_user_data_id_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[{"user_id": "123e4567-e89b-12d3-a456-426614174000"}])
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/users/by_user_data/123e4567-e89b-12d3-a456-426614174000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"user_id": "123e4567-e89b-12d3-a456-426614174000"})


if __name__ == '__main__':
    unittest.main()