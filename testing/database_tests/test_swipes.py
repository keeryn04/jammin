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
        mock_conn.table.return_value.select.return_value.execute.return_value = [
            {
                "swipe_id": "123", 
                "swiper_id": "user1", 
                "swiped_id": "user2", 
                "action": "like"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get('/api/swipes')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"swipe_id": "123", "swiper_id": "user1", "swiped_id": "user2", "action": "like"}
        ])

    @patch('api.routes.swipes.get_db_connection')
    def test_get_swipe_success(self, mock_get_db_connection):
        # Generate a valid UUID for the swipe_id
        swipe_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = [
            {
                "swipe_id": swipe_id, 
                "swiper_id": "user1", 
                "swiped_id": "user2", 
                "action": "like"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get(f'/api/swipes/{swipe_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"swipe_id": swipe_id, "swiper_id": "user1", "swiped_id": "user2", "action": "like"}
        ])

    @patch('api.routes.swipes.get_db_connection')
    # Fails in main due to the add_swipe method needing a swipe_id argument
    # (which is not necessary)
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


if __name__ == '__main__':
    unittest.main()