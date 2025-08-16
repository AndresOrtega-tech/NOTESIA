from supabase import create_client, Client
from app.config import settings

# Supabase Client
supabase: Client = create_client (
    settings.supabase_url,
    settings.supabase_key
)

# Service Client
supabase_admin: Client = create_client (
    settings.supabase_url,
    settings.supabase_service_key
)

def get_supabase_client() -> Client:
    """Returns the Supabase client. """
    return supabase

def get_supabase_admin_client() -> Client:
    """Returns the Supabase admin client. """
    return supabase_admin

