import os
import sys
import uuid  # Import the uuid module to generate valid UUIDs

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
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.execute.return_value = MagicMock(data=[
            {"user_data_id": "123", "spotify_id": "spotify123", "top_songs": "song1, song2"}
        ])
        mock_get_db_connection.return_value = mock_conn

        response = self.client.get('/api/user_data')
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
    def test_update_user_data_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_conn.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock(data={"id": 1})
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
    # Will fail on main due to the line: "if isinstance(response, dict) and "error" in response:"
    # This is because the response is being accessed prior to being initialized
    # Possible solution: move the specified statement to just before the return statement
    # and change the return to return jsonify(response), 200 
    def test_get_user_music_data_by_id_success(self, mock_get_db_connection):
        # Generate a valid UUID for the user_id
        user_id = str(uuid.uuid4())
        mock_data = [
            {
                "user_id": user_id, 
                "top_songs": "song1, song2", 
                "top_artists": "artist1, artist2", 
                "top_genres": "genre1, genre2"
            }
        ]
    

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_data
        
        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get(f'/api/user_data/{user_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "user_id": user_id,
            "music_profile": {
                "top_songs": "song1, song2",
                "top_artists": "artist1, artist2",
                "top_genres": "genre1, genre2"
            }
        })

    @patch('api.routes.user_data.get_db_connection')
    # Will fail on main due to the line: "if isinstance(response, dict) and "error" in response:"
    # This is because the response is being accessed prior to being initialized
    # Possible solution: move the specified statement to just before the return statement
    # and change the return to return jsonify(response), 200
    # There is also a small inconsistency in the data accessing (must use row[0]["top_artists"].split(", ")[:limit]).
    def test_get_user_top_artists_by_id_success(self, mock_get_db_connection):
        # Generate a valid UUID for the user_id
        user_id = str(uuid.uuid4())
        mock_data = [
            {
                "top_artists": "artist1, artist2, artist3",
                "top_artists_pictures": "pic1, pic2, pic3"
            }
        ]

        # Mock the database connection and response
        mock_conn = MagicMock()
        mock_conn.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_data

        mock_get_db_connection.return_value = mock_conn

        # Send the GET request
        response = self.client.get(f'/api/user_data/{user_id}/2')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "user_id": user_id,
            "top_artists": ["artist1", "artist2"],
            "top_artists_pictures": ["pic1", "pic2"]
        })

if __name__ == '__main__':
    unittest.main()