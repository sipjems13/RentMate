from fastapi import FastAPI
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://rdzmlzrsvmewwizimgnb.supabase.co"
SUPABASE_KEY = "sb_publishable_rD3RjsKnJAtMOlGggsFr9g_rK9RitvU"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/users")
def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@app.post("/users")
def add_user(name: str, email: str):
    response = supabase.table("users").insert({"name": name, "email": email}).execute()
    return response.data
