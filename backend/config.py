#backend/config.py
#loads enviornement variables

from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
