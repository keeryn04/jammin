from supabase import create_client, Client
from mockito import when, patch, unstub, mock
import unittest

class TestDBUsers(unittest.TestCase):
    def setUp(self):
        self.mock_client = mock(Client)

    def test_get_users(self):
        when(create_client).thenReturn(self.mock_client)