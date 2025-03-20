import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.routes.user_settings import user_setting_routes
import uuid

class TestUserSettingsRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(user_setting_routes)
        self.client = self.app.test_client()

    @patch('api.routes.user_settings.get_db_connection')
    def test_get_user_settings_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.return_value = [
            {
                "setting_id": "123", 
                "user_id": "user1", 
                "discoverability": True, 
                "notifications": True, 
                "theme_preference": "light", 
                "language": "en"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get('/api/user_settings')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"setting_id": "123", "user_id": "user1", "discoverability": True, "notifications": True, "theme_preference": "light", "language": "en"}
        ])

    @patch('api.routes.user_settings.get_db_connection')
    def test_get_user_setting_success(self, mock_get_db_connection):
        # Generate a valid UUID for the setting_id
        setting_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = [
            {
                "setting_id": setting_id, 
                "user_id": "user1", 
                "discoverability": True, 
                "notifications": True, 
                "theme_preference": "light", 
                "language": "en"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get(f'/api/user_settings/{setting_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"setting_id": setting_id, "user_id": "user1", "discoverability": True, "notifications": True, "theme_preference": "light", "language": "en"}
        ])

    @patch('api.routes.user_settings.get_db_connection')
    def test_add_user_settings_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.insert.return_value.execute.return_value = {"data": {"setting_id": "123"}}
        mock_get_db_connection.return_value = mock_conn

        # Define the user settings data to be sent in the request
        user_settings_data = {
            "user_id": "user1",
            "discoverability": True,
            "notifications": True,
            "theme_preference": "dark",
            "language": "fr"
        }

        # Send the POST request
        response = self.client.post('/api/user_settings', json=user_settings_data)

        # Assert the response
        self.assertEqual(response.status_code, 201)
        self.assertIn("User settings added successfully", response.json["message"])

    @patch('api.routes.user_settings.get_db_connection')
    def test_update_user_settings_success(self, mock_get_db_connection):
        # Generate a valid UUID for the setting_id
        setting_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.update.return_value.eq.return_value.execute.return_value = {"data": {"setting_id": setting_id}}
        mock_get_db_connection.return_value = mock_conn

        # Define the user settings data to be sent in the request
        user_settings_data = {
            "user_id": "user1",
            "discoverability": False,
            "notifications": False,
            "theme_preference": "light",
            "language": "en"
        }

        # Send the PUT request
        response = self.client.put(f'/api/user_settings/{setting_id}', json=user_settings_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("User Settings updated successfully", response.json["message"])

    @patch('api.routes.user_settings.get_db_connection')
    def test_delete_user_settings_success(self, mock_get_db_connection):
        # Generate a valid UUID for the setting_id
        setting_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = {"data": {"setting_id": setting_id}}
        mock_get_db_connection.return_value = mock_conn

        # Send the DELETE request
        response = self.client.delete(f'/api/user_settings/{setting_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Settings deleted successfully", response.json["message"])


if __name__ == '__main__':
    unittest.main()