import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
from api.database_connector import get_db_connection

class TestDatabaseConnector(unittest.TestCase):

    @patch('api.database_connector.create_client')
    def test_get_db_connection_success(self, mock_create_client):
        # Arrange
        mock_supabase = MagicMock()
        mock_create_client.return_value = mock_supabase

        # Act
        result = get_db_connection()

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, mock_supabase)
        mock_create_client.assert_called_once()

    @patch('api.database_connector.create_client')
    def test_get_db_connection_failure(self, mock_create_client):
        # Arrange
        mock_create_client.side_effect = Exception("Connection error")

        # Act
        result = get_db_connection()

        # Assert
        self.assertIsNone(result)
        mock_create_client.assert_called_once()

if __name__ == '__main__':
    unittest.main()