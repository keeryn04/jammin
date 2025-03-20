import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.routes.matches import matches_routes
import uuid

class TestMatchesRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(matches_routes)
        self.client = self.app.test_client()

    @patch('api.routes.matches.get_db_connection')
    def test_get_matches_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.return_value = [
            {
                "match_id": "123", 
                "user_1_id": "user1", 
                "user_2_id": "user2", 
                "match_score": 85, 
                "status": "active", 
                "reasoning": "Shared interests"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get('/api/matches')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"match_id": "123", "user_1_id": "user1", "user_2_id": "user2", "match_score": 85, "status": "active", "reasoning": "Shared interests"}
        ])

    @patch('api.routes.matches.get_db_connection')
    def test_get_match_success(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = [
            {
                "match_id": match_id, 
                "user_1_id": "user1", 
                "user_2_id": "user2", 
                "match_score": 85, 
                "status": "active", 
                "reasoning": "Shared interests"
            }
        ]
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get(f'/api/matches/{match_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"match_id": match_id, "user_1_id": "user1", "user_2_id": "user2", "match_score": 85, "status": "active", "reasoning": "Shared interests"}
        ])

    @patch('api.routes.matches.get_db_connection')
    def test_add_match_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.upsert.return_value.execute.return_value = {"data": {"match_id": "123"}}
        mock_get_db_connection.return_value = mock_conn

        # Define the match data to be sent in the request
        match_data = {
            "user_1_id": "user1",
            "user_2_id": "user2",
            "match_score": 85,
            "status": "active",
            "reasoning": "Shared interests"
        }

        # Send the POST request
        response = self.client.post('/api/matches', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Match added successfully", response.json["message"])

    @patch('api.routes.matches.get_db_connection')
    def test_update_match_success(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.update.return_value.eq.return_value.execute.return_value = {"data": {"match_id": match_id}}
        mock_get_db_connection.return_value = mock_conn

        # Define the match data to be sent in the request
        match_data = {
            "user_1_id": "user1",
            "user_2_id": "user2",
            "match_score": 90,
            "status": "inactive",
            "reasoning": "No longer compatible"
        }

        # Send the POST request
        response = self.client.post(f'/api/matches/{match_id}', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Match updated successfully", response.json["message"])

    @patch('api.routes.matches.get_db_connection')
    def test_delete_match_success(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = {"data": {"match_id": match_id}}
        mock_get_db_connection.return_value = mock_conn

        # Send the DELETE request
        response = self.client.delete(f'/api/matches/{match_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Match deleted successfully", response.json["message"])


if __name__ == '__main__':
    unittest.main()