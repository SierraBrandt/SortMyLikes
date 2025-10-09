#backend/spotify_utils.py
#functions to get liked songs, audio features, create playlists

import json
import spotipy

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
            "id": track['id'],
            "uri": track['uri']
        })
    return liked_songs
