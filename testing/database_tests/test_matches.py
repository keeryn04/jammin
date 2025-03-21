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

    # ============== GET /api/matches Tests ==============
    @patch('api.routes.matches.get_db_connection')
    def test_get_matches_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        
        # Create a mock response object with a data attribute
        mock_response = MagicMock()
        mock_response.data = [
            {
                "match_id": "123",
                "user_1_id": "user1",
                "user_2_id": "user2",
                "match_score": 85,
                "status": "active",
                "reasoning": "Shared interests"
            }
        ]
        
        mock_conn.table.return_value.select.return_value.execute.return_value = mock_response
        
        mock_get_db_connection.return_value = mock_conn
        # Send the GET request
        response = self.client.get('/api/matches')
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"match_id": "123", "user_1_id": "user1", "user_2_id": "user2", "match_score": 85, "status": "active", "reasoning": "Shared interests"}
        ])

    @patch('api.routes.matches.get_db_connection')
    def test_get_matches_db_connection_error(self, mock_get_db_connection):
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the GET request
        response = self.client.get('/api/matches')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Unable to connect to the database"})

    @patch('api.routes.matches.get_db_connection')
    def test_get_matches_db_error(self, mock_get_db_connection):
        # Mock database query error
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.side_effect = Exception("Database error")
        mock_get_db_connection.return_value = mock_conn
        
        # Send the GET request
        response = self.client.get('/api/matches')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Database error" in response.json["error"])

    @patch('api.routes.matches.get_db_connection')
    def test_get_matches_supabase_error(self, mock_get_db_connection):
        # Mock Supabase error response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.return_value = {
            "error": {"message": "Supabase error occurred"}
        }
        mock_get_db_connection.return_value = mock_conn
        
        # Send the GET request
        response = self.client.get('/api/matches')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Supabase error occurred" in response.json["error"])

    # ============== GET /api/matches/<match_id> Tests ==============
    @patch('api.routes.matches.get_db_connection')
    def test_get_match_success(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock the database connection and response
        mock_conn = MagicMock()
        
        # Create a mock response object with a data attribute
        mock_response = MagicMock()
        mock_response.data = [
            {
                "match_id": match_id,
                "user_1_id": "user1",
                "user_2_id": "user2",
                "match_score": 85,
                "status": "active",
                "reasoning": "Shared interests"
            }
        ]
        
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response
        
        mock_get_db_connection.return_value = mock_conn
        # Send the GET request
        response = self.client.get(f'/api/matches/{match_id}')
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"match_id": match_id, "user_1_id": "user1", "user_2_id": "user2", "match_score": 85, "status": "active", "reasoning": "Shared interests"}
        ])

    @patch('api.routes.matches.get_db_connection')
    def test_get_match_invalid_id(self, mock_get_db_connection):
        # Use an invalid UUID
        match_id = "not-a-valid-uuid"
        
        # Mock the database connection
        mock_get_db_connection.return_value = MagicMock()
        
        # Send the GET request
        response = self.client.get(f'/api/matches/{match_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid match_id format"})

    @patch('api.routes.matches.get_db_connection')
    def test_get_match_db_connection_error(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the GET request
        response = self.client.get(f'/api/matches/{match_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Unable to connect to the database"})

    # ============== POST /api/matches Tests ==============
    @patch('api.routes.matches.get_db_connection')
    def test_add_match_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.upsert.return_value.execute.return_value = {"data": {"match_id": "123"}}
        mock_get_db_connection.return_value = mock_conn

        # Define the match data to be sent in the request
        match_data = {
            "user_1_data_id": "user1",
            "user_2_data_id": "user2",
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
    def test_add_match_missing_data(self, mock_get_db_connection):
        # Mock the database connection
        mock_get_db_connection.return_value = MagicMock()

        # Define incomplete match data
        match_data = {
            "user_1_data_id": "user1",
            # Missing user_2_data_id
            "match_score": 85,
            "status": "active"
            # Missing reasoning
        }

        # Send the POST request
        response = self.client.post('/api/matches', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Database error" in response.json["error"])

    @patch('api.routes.matches.get_db_connection')
    def test_add_match_db_connection_error(self, mock_get_db_connection):
        # Mock database connection failure
        mock_get_db_connection.return_value = None

        # Define the match data
        match_data = {
            "user_1_data_id": "user1",
            "user_2_data_id": "user2",
            "match_score": 85,
            "status": "active",
            "reasoning": "Shared interests"
        }

        # Send the POST request
        response = self.client.post('/api/matches', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Unable to connect to the database"})

    @patch('api.routes.matches.get_db_connection')
    def test_add_match_supabase_error(self, mock_get_db_connection):
        # Mock Supabase error response
        mock_conn = MagicMock()
        mock_conn.table.return_value.upsert.return_value.execute.return_value = {
            "error": {"message": "Supabase error occurred"}
        }
        mock_get_db_connection.return_value = mock_conn

        # Define the match data
        match_data = {
            "user_1_data_id": "user1",
            "user_2_data_id": "user2",
            "match_score": 85,
            "status": "active",
            "reasoning": "Shared interests"
        }

        # Send the POST request
        response = self.client.post('/api/matches', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Supabase error occurred" in response.json["error"])

    # ============== PUT /api/matches/<match_id> Tests ==============
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

        # Send the PUT request
        response = self.client.put(f'/api/matches/{match_id}', json=match_data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Match updated successfully", response.json["message"])

    @patch('api.routes.matches.get_db_connection')
    def test_update_match_invalid_id(self, mock_get_db_connection):
        # Use an invalid UUID
        match_id = "not-a-valid-uuid"
        
        # Mock the database connection
        mock_get_db_connection.return_value = MagicMock()
        
        # Define the match data
        match_data = {
            "user_1_id": "user1",
            "user_2_id": "user2",
            "match_score": 90,
            "status": "inactive",
            "reasoning": "No longer compatible"
        }
        
        # Send the PUT request
        response = self.client.put(f'/api/matches/{match_id}', json=match_data)
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid match_id format"})

    @patch('api.routes.matches.get_db_connection')
    def test_update_match_empty_json(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock the database connection
        mock_get_db_connection.return_value = MagicMock()
        
        # Send the PUT request with empty JSON
        response = self.client.put(f'/api/matches/{match_id}', json={})
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid JSON data"})

    @patch('api.routes.matches.get_db_connection')
    def test_update_match_db_connection_error(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Define the match data
        match_data = {
            "user_1_id": "user1",
            "user_2_id": "user2",
            "match_score": 90,
            "status": "inactive",
            "reasoning": "No longer compatible"
        }
        
        # Send the PUT request
        response = self.client.put(f'/api/matches/{match_id}', json=match_data)
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Unable to connect to the database"})

    # ============== DELETE /api/matches/<match_id> Tests ==============
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

    @patch('api.routes.matches.get_db_connection')
    def test_delete_match_invalid_id(self, mock_get_db_connection):
        # Use an invalid UUID
        match_id = "not-a-valid-uuid"
        
        # Mock the database connection
        mock_get_db_connection.return_value = MagicMock()
        
        # Send the DELETE request
        response = self.client.delete(f'/api/matches/{match_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid match_id format"})

    @patch('api.routes.matches.get_db_connection')
    def test_delete_match_db_connection_error(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock database connection failure
        mock_get_db_connection.return_value = None
        
        # Send the DELETE request
        response = self.client.delete(f'/api/matches/{match_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Unable to connect to the database"})

    @patch('api.routes.matches.get_db_connection')
    def test_delete_match_supabase_error(self, mock_get_db_connection):
        # Generate a valid UUID for the match_id
        match_id = str(uuid.uuid4())
        
        # Mock Supabase error response
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = {
            "error": {"message": "Supabase error occurred"}
        }
        mock_get_db_connection.return_value = mock_conn
        
        # Send the DELETE request
        response = self.client.delete(f'/api/matches/{match_id}')
        
        # Assert the response
        self.assertEqual(response.status_code, 500)
        self.assertTrue("Supabase error occurred" in response.json["error"])


if __name__ == '__main__':
    unittest.main()