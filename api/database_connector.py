import os
from dotenv import load_dotenv
from supabase import create_client, Client

#Get environment variables for MySQL connection
load_dotenv()

#Get Supabase connection things from environment file
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

#Test database connection
def get_db_connection():
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        return supabase
    except Exception as e:
        print(f"Supabase connection error: {e}")
        return None