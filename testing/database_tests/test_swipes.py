import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.routes.swipes import swipes_routes
import uuid

class TestSwipesRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(swipes_routes)
        self.client = self.app.test_client()

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipes_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        
        # Create a mock response object with a data attribute
        mock_response = MagicMock()
        mock_response.data = [
            {
                "swipe_id": "123",
                "swiper_id": "user1",
                "swiped_id": "user2",
                "action": "like"
            }
        ]
        
        mock_conn.table.return_value.select.return_value.execute.return_value = mock_response
        
        mock_get_db_connection.return_value = mock_conn
        # Send the GET request
        response = self.client.get('/api/swipes')
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"swipe_id": "123", "swiper_id": "user1", "swiped_id": "user2", "action": "like"}
        ])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipes_db_connection_failure(self, mock_get_db_connection):
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the GET request
        response = self.client.get('/api/swipes')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipes_db_error(self, mock_get_db_connection):
        # Mock the database connection and error response
        mock_conn = MagicMock()
        
        # Set up a database error
        mock_conn.table.return_value.select.return_value.execute.side_effect = Exception("Database error occurred")
        
        mock_get_db_connection.return_value = mock_conn
        
        # Send the GET request
        response = self.client.get('/api/swipes')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipe_success(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())
        
        # Mock the database connection and response
        mock_conn = MagicMock()
        
        # Create a mock response object with a data attribute
        mock_response = MagicMock()
        mock_response.data = [
            {
                "swipe_id": swipe_id,
                "swiper_id": "user1",
                "swiped_id": "user2",
                "action": "like"
            }
        ]
        
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        mock_get_db_connection.return_value = mock_conn
        # Send the GET request
        response = self.client.get(f'/api/swipes/{swipe_id}')
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"swipe_id": swipe_id, "swiper_id": "user1", "swiped_id": "user2", "action": "like"}
        ])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipe_invalid_uuid(self, mock_get_db_connection):
        # Setup a mock connection so we get to the UUID validation step
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        
        # Test with an invalid UUID
        invalid_swipe_id = "not-a-uuid"
        
        # Send the GET request
        response = self.client.get(f'/api/swipes/{invalid_swipe_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user_id format", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipe_db_connection_failure(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())
        
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the GET request
        response = self.client.get(f'/api/swipes/{swipe_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_add_swipe_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.upsert.return_value.execute.return_value = {"data": {"swipe_id": "123"}}
        mock_get_db_connection.return_value = mock_conn

        # Define the swipe data to be sent in the request
        swipe_data = {
            "swiper_id": "user1",
            "swiped_id": "user2",
            "action": "like"
        }

        # Send the POST request
        response = self.client.post('/api/swipes', json=swipe_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Swipe recorded successfully", response.json["message"])

    @patch('api.routes.swipes.get_db_connection')
    def test_add_swipe_missing_data(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Define incomplete swipe data
        incomplete_data = {
            "swiper_id": "user1",
            # Missing swiped_id
            "action": "like"
        }

        # Send the POST request
        response = self.client.post('/api/swipes', json=incomplete_data)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_add_swipe_db_connection_failure(self, mock_get_db_connection):
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Define the swipe data
        swipe_data = {
            "swiper_id": "user1",
            "swiped_id": "user2",
            "action": "like"
        }
        
        # Send the POST request
        response = self.client.post('/api/swipes', json=swipe_data)
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_update_swipe_success(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.update.return_value.eq.return_value.execute.return_value = {"data": {"swipe_id": swipe_id}}
        mock_get_db_connection.return_value = mock_conn

        # Define the swipe data to be sent in the request
        swipe_data = {
            "swiper_id": "user1",
            "swiped_id": "user2",
            "action": "dislike"
        }

        # Send the POST request
        response = self.client.post(f'/api/swipes/{swipe_id}', json=swipe_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Swipe updated successfully", response.json["message"])

    @patch('api.routes.swipes.get_db_connection')
    def test_update_swipe_invalid_uuid(self, mock_get_db_connection):
        # Setup a mock connection so we get to the UUID validation step
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        
        # Test with an invalid UUID
        invalid_swipe_id = "not-a-uuid"
        
        # Define the swipe data
        swipe_data = {
            "swiper_id": "user1",
            "swiped_id": "user2",
            "action": "dislike"
        }
        
        # Send the POST request
        response = self.client.post(f'/api/swipes/{invalid_swipe_id}', json=swipe_data)
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid swipe_id format", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_update_swipe_missing_data(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())
        
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        
        # Define incomplete swipe data
        incomplete_data = {
            "swiper_id": "user1",
            # Missing swiped_id
            "action": "dislike"
        }
        
        # Send the POST request
        response = self.client.post(f'/api/swipes/{swipe_id}', json=incomplete_data)
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_delete_swipe_success(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = {"data": {"swipe_id": swipe_id}}
        mock_get_db_connection.return_value = mock_conn

        # Send the DELETE request
        response = self.client.delete(f'/api/swipes/{swipe_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Swipe deleted successfully", response.json["message"])

    @patch('api.routes.swipes.get_db_connection')
    def test_delete_swipe_invalid_uuid(self, mock_get_db_connection):
        # Setup a mock connection so we get to the UUID validation step
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        
        # Test with an invalid UUID
        invalid_swipe_id = "not-a-uuid"
        
        # Send the DELETE request
        response = self.client.delete(f'/api/swipes/{invalid_swipe_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid swipe_id format", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_delete_swipe_db_error(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())
        
        # Mock the database connection and error response
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.side_effect = Exception("Database error occurred")
        mock_get_db_connection.return_value = mock_conn
        
        # Send the DELETE request
        response = self.client.delete(f'/api/swipes/{swipe_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.swipes.get_db_connection')
    def test_delete_swipe_db_connection_failure(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())
        
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the DELETE request
        response = self.client.delete(f'/api/swipes/{swipe_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])


if __name__ == '__main__':
    unittest.main()