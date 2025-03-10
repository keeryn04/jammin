import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mockito import when, patch, unstub, mock
import unittest
from api.database_connector import get_db_connection
import mysql.connector
from flask.cli import load_dotenv

class TestDBConnector(unittest.TestCase):
    def test_db_connector(self):    
        print("Running test_db_connector") 
        mock_conn = mock(mysql.connector.connection.MySQLConnection)
    
        when(mysql.connector).connect(
            host=None,
            user=None,
            password=None,
            database=None
        ).thenReturn(mock_conn)

        test_conn = get_db_connection()

        self.assertIsInstance(test_conn, mysql.connector.connection.MySQLConnection, "Must return a MySQLConnection object")
        unstub()

    def test_db_connector_fail(self):  

        print("Running test_db_connector_fail")
        when(mysql.connector).connect(
            host=None,
            user=None,
            password=None,
            database=None
        ).thenRaise(mysql.connector.Error("Connection Error"))
        
        test_conn = get_db_connection()
        self.assertEqual(test_conn, None, "Must return None")
        unstub()

if __name__ == "__main__":
    unittest.main()