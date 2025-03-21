import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from unittest.mock import patch, MagicMock
import os
from io import StringIO
import sys

# Import the modules to test
from database.database_connector import SupabaseSingleton, get_db_connection

class TestSupabaseConnection(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        SupabaseSingleton._instance = None
        
        # Prepare environment for testing
        self.original_environ = os.environ.copy()
        os.environ["VITE_SUPABASE_URL"] = "https://test-url.supabase.co"
        os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
        
    def tearDown(self):
        # Restore original environment after each test
        os.environ.clear()
        os.environ.update(self.original_environ)
        
        # Reset the singleton instance after each test
        SupabaseSingleton._instance = None
    
    @patch('supabase.create_client')
    def test_get_instance_success(self, mock_create_client):
        # Arrange
        mock_client = MagicMock()
        mock_create_client.return_value = mock_client
        
        # Make sure instance is None before the test
        SupabaseSingleton._instance = None
        
        # Act
        result = SupabaseSingleton.get_instance()
        
        # Assert - verify that the singleton instance was set properly
        self.assertEqual(SupabaseSingleton._instance, mock_client)
        self.assertEqual(result, mock_client)
        mock_create_client.assert_called_once_with(
            "https://test-url.supabase.co", 
            "test-service-key"
        )
        
        # Test that the instance is reused (singleton behavior)
        mock_create_client.reset_mock()
        second_result = SupabaseSingleton.get_instance()
        self.assertEqual(second_result, mock_client)
        mock_create_client.assert_not_called()
    
    @patch('supabase.create_client')
    def test_get_instance_missing_env_vars(self, mock_create_client):
        # Arrange
        os.environ.pop("VITE_SUPABASE_URL", None)
        
        # Capture stdout to verify error message
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Act
        result = SupabaseSingleton.get_instance()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Assert
        self.assertIsNone(result)
        self.assertIn("Supabase connection error", captured_output.getvalue())
        self.assertIn("Supabase URL or Service Key is missing", captured_output.getvalue())
        mock_create_client.assert_not_called()
    
    @patch('supabase.create_client')
    def test_get_instance_connection_error(self, mock_create_client):
        # Arrange
        mock_create_client.side_effect = Exception("Any error message")
        
        # Capture stdout to verify error message
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Act
        result = SupabaseSingleton.get_instance()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Assert
        self.assertIsNone(result)
        self.assertIn("Supabase connection error", captured_output.getvalue())
    
    @patch('database.database_connector.SupabaseSingleton.get_instance')
    def test_get_db_connection(self, mock_get_instance):
        # Arrange
        mock_client = MagicMock()
        mock_get_instance.return_value = mock_client
        
        # Act
        result = get_db_connection()
        
        # Assert
        self.assertEqual(result, mock_client)
        mock_get_instance.assert_called_once()

if __name__ == '__main__':
    unittest.main()