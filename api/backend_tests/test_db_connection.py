import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mockito import when, patch, unstub, mock
import unittest
from api.database_connector import get_db_connection
import mysql.connector

class TestDBConnector(unittest.TestCase):
    def test_db_connector(self):     
        mock_conn = mock(mysql.connector.connection.MySQLConnection)
        
        when(mysql.connector).connect(
            host='localhost',
            user='root',
            password='password',
            database='jammin_db'
        ).thenReturn(mock_conn)

        actual_conn = get_db_connection()

        self.assertIsInstance(actual_conn, mysql.connector.connection.MySQLConnection, "Must be the same")
        unstub()

    def test_db_connector_fail(self):     
        actual_conn = get_db_connection()
        
        mock_conn = mock(None)
        
        when(mysql.connector).connect(
            host='localhost',
            user='root',
            password='password',
            database='jammin_db'
        ).thenReturn(mock_conn)

        test_conn = get_db_connection()

        self.assertIsInstance(actual_conn, None, "Must be the same")
        unstub()

if __name__ == "__main__":
    unittest.main()