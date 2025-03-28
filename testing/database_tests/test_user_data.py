import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.routes.user_data import user_data_routes

class TestUserDataRoutes(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(user_data_routes)
        self.client = self.app.test_client()

    @patch('api.routes.user_data.get_db_connection')
    def test_get_users_data_success(self, mock_get_db_connection):
        # Mock the database connection and response
        mock_conn = MagicMock()
        
        # Create a mock response object with a data attribute
        mock_response = MagicMock()
        mock_response.data = [
            {
                "user_data_id": "123", 
                "spotify_id": "spotify123", 
                "top_songs": "song1, song2"
            }
        ]
        
        mock_conn.table.return_value.select.return_value.execute.return_value = mock_response
        
        mock_get_db_connection.return_value = mock_conn
        # Send the GET request
        response = self.client.get('/api/user_data')
        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"user_data_id": "123", "spotify_id": "spotify123", "top_songs": "song1, song2"}
        ])

    @patch('api.routes.user_data.get_db_connection')
    def test_get_users_data_failure(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        response = self.client.get('/api/user_data')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_get_users_data_db_error(self, mock_get_db_connection):
        # Mock a database error in the response
        mock_conn = MagicMock()
        mock_response = {"error": {"message": "Database query failed"}}
        mock_conn.table.return_value.select.return_value.execute.return_value = mock_response
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/user_data')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_get_users_data_exception(self, mock_get_db_connection):
        # Mock an exception during database operation
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.side_effect = Exception("Connection timeout")
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/user_data')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_add_user_data_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.insert.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_get_db_connection.return_value = mock_conn

        user_data = {
            "user_id": "user123",
            "spotify_id": "spotify123",
            "top_songs": "song1, song2",
            "top_songs_pictures": "pic1, pic2",
            "top_artists": "artist1, artist2",
            "top_artists_pictures": "artist_pic1, artist_pic2",
            "top_genres": "genre1, genre2",
            "top_genres_pictures": "genre_pic1, genre_pic2",
            "profile_name": "Test User",
            "profile_image": "profile_pic_url"
        }

        response = self.client.post('/api/user_data', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User data entry added successfully", response.json["message"])

    @patch('api.routes.user_data.get_db_connection')
    def test_add_user_data_missing_fields(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Missing required field
        incomplete_data = {
            "user_id": "user123",
            "spotify_id": "spotify123",
            # Missing other required fields
        }

        response = self.client.post('/api/user_data', json=incomplete_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_add_user_data_db_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_response = {"error": {"message": "Duplicate entry"}}
        mock_conn.table.return_value.insert.return_value.execute.return_value = mock_response
        mock_get_db_connection.return_value = mock_conn

        user_data = {
            "user_id": "user123",
            "spotify_id": "spotify123",
            "top_songs": "song1, song2",
            "top_songs_pictures": "pic1, pic2",
            "top_artists": "artist1, artist2",
            "top_artists_pictures": "artist_pic1, artist_pic2",
            "top_genres": "genre1, genre2",
            "top_genres_pictures": "genre_pic1, genre_pic2",
            "profile_name": "Test User",
            "profile_image": "profile_pic_url"
        }

        response = self.client.post('/api/user_data', json=user_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_update_user_data_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.insert.return_value.eq.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_get_db_connection.return_value = mock_conn

        # Generate a valid UUID for the user_data_id
        user_data_id = str(uuid.uuid4())

        user_data = {
            "spotify_id": "spotify123",
            "top_songs": "song1, song2",
            "top_songs_pictures": "pic1, pic2",
            "top_artists": "artist1, artist2",
            "top_artists_pictures": "artist_pic1, artist_pic2",
            "top_genres": "genre1, genre2",
            "top_genres_pictures": "genre_pic1, genre_pic2",
            "profile_name": "Updated User",
            "profile_image": "updated_profile_pic_url"
        }

        response = self.client.put(f'/api/user_data/{user_data_id}', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User Settings updated successfully", response.json["message"])

    @patch('api.routes.user_data.get_db_connection')
    def test_update_user_data_invalid_uuid(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Invalid UUID format
        invalid_user_data_id = "not-a-valid-uuid"

        user_data = {
            "spotify_id": "spotify123",
            "top_songs": "song1, song2",
            "top_songs_pictures": "pic1, pic2",
            "top_artists": "artist1, artist2",
            "top_artists_pictures": "artist_pic1, artist_pic2",
            "top_genres": "genre1, genre2",
            "top_genres_pictures": "genre_pic1, genre_pic2",
            "profile_name": "Updated User",
            "profile_image": "updated_profile_pic_url"
        }

        response = self.client.put(f'/api/user_data/{invalid_user_data_id}', json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user_data_id format", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_update_user_data_missing_fields(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Generate a valid UUID for the user_data_id
        user_data_id = str(uuid.uuid4())

        # Missing required fields
        incomplete_data = {
            "spotify_id": "spotify123",
            # Missing other required fields
        }

        response = self.client.put(f'/api/user_data/{user_data_id}', json=incomplete_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_update_user_data_db_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        # Note: The real code uses response.error.message but the test should mock response as a dict
        # to match how the error is checked in the code
        mock_conn.table.return_value.insert.return_value.eq.return_value.execute.return_value = {"error": {"message": "Record not found"}}
        mock_get_db_connection.return_value = mock_conn

        user_data_id = str(uuid.uuid4())
        user_data = {
            "spotify_id": "spotify123",
            "top_songs": "song1, song2",
            "top_songs_pictures": "pic1, pic2",
            "top_artists": "artist1, artist2",
            "top_artists_pictures": "artist_pic1, artist_pic2",
            "top_genres": "genre1, genre2",
            "top_genres_pictures": "genre_pic1, genre_pic2",
            "profile_name": "Updated User",
            "profile_image": "updated_profile_pic_url"
        }

        response = self.client.put(f'/api/user_data/{user_data_id}', json=user_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_delete_user_data_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock(data={"id": 1})
        mock_get_db_connection.return_value = mock_conn

        # Generate a valid UUID for the user_data_id
        user_data_id = str(uuid.uuid4())

        response = self.client.delete(f'/api/user_data/{user_data_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Music data deleted successfully", response.json["message"])

    @patch('api.routes.user_data.get_db_connection')
    def test_delete_user_data_invalid_uuid(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn

        # Invalid UUID format
        invalid_user_data_id = "not-a-valid-uuid"

        response = self.client.delete(f'/api/user_data/{invalid_user_data_id}')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid user_data_id format", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_delete_user_data_db_error(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.delete.return_value.eq.return_value.execute.return_value = {"error": {"message": "Record not found"}}
        mock_get_db_connection.return_value = mock_conn

        user_data_id = str(uuid.uuid4())

        response = self.client.delete(f'/api/user_data/{user_data_id}')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json["error"])

    @patch('api.routes.user_data.get_db_connection')
    def test_delete_user_data_no_connection(self, mock_get_db_connection):
        mock_get_db_connection.return_value = None

        user_data_id = str(uuid.uuid4())

        response = self.client.delete(f'/api/user_data/{user_data_id}')
        self.assertEqual(response.status_code, 500)
        self.assertIn("Unable to connect to the database", response.json["error"])

if __name__ == '__main__':
    unittest.main()