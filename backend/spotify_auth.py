#backend/spotify_auth.py
#Handles Spotify OAuth setup and token management

from spotipy import SpotifyOAuth
from dotenv import load_dotenv 
import os

load_dotenv()
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read playlist-modify-public playlist-modify-private"
)
