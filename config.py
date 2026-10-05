import os
from dotenv import load_dotenv

load_dotenv()

ROBLOX_CLIENT_ID = os.getenv("ROBLOX_CLIENT_ID")
ROBLOX_CLIENT_SECRET = os.getenv("ROBLOX_CLIENT_SECRET")
ROBLOX_AUTH_URL = os.getenv("ROBLOX_AUTH_URL")
ROBLOX_REDIRECT_URI = os.getenv("ROBLOX_REDIRECT_URI", "http://localhost:8000/auth/roblox/callback")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")