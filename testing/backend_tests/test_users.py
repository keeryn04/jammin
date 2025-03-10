import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mockito import when, patch, unstub, mock
import unittest
from api.database_connector import get_db_connection
import mysql.connector
from flask.cli import load_dotenv
from api.routes.users import user_routes

class TestDBUsers(unittest.TestCase):
    def test_get_users(self):
        mock_conn = mock(mysql.connector.connection.MySQLConnection)
    
        when(mysql.connector).connect(
            host=None,
            user=None,
            password=None,
            database=None
        ).thenReturn(mock_conn)

        
