import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class SupabaseSingleton:
    _instance: Client = None

    @classmethod
    def get_instance(cls) -> Client:
        """Returns a singleton instance of the Supabase client."""
        if cls._instance is None:
            try:
                supabase_url = os.getenv("VITE_SUPABASE_URL")
                supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

                if not supabase_url or not supabase_service_key:
                    raise ValueError("Supabase URL or Service Key is missing.")

                cls._instance = create_client(supabase_url, supabase_service_key)
            except Exception as e:
                print(f"Supabase connection error: {e}")
                cls._instance = None
        return cls._instance

def get_db_connection() -> Client:
    """Returns the singleton instance of the Supabase client."""
    return SupabaseSingleton.get_instance()