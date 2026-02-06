#backend/spotify_utils.py
#functions to get liked songs, audio features, create playlists

import json
import spotipy
import time
from spotify_auth import sp_oauth

def get_liked_tracks():
    token_info = json.load(open("token_info.json"))
    sp = spotipy.Spotify(auth=token_info["access_token"])
    results = sp.current_user_saved_tracks(limit=50)

    liked_songs = []
    for item in results['items']:
        track = item['track']
        liked_songs.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "artist_id": track['artists'][0]['id'],
            "id": track['id'],
            "uri": track['uri']
        })

    return liked_songs

def get_valid_token():
    token_info = json.load(open("token_info.json"))

    # If expired, refresh
    if token_info.get("expires_at") and token_info["expires_at"] - int(time.time()) < 60:
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        with open("token_info.json", "w") as f:
            json.dump(token_info, f)

    return token_info["access_token"]

def get_spotify_client():
    access_token = get_valid_token()
    return spotipy.Spotify(auth=access_token)