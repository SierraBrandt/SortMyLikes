# backend/playlist_ai.py

import spotipy
import json
from spotify_utils import get_spotify_client
from collections import defaultdict

GENRE_BUCKETS = {
    "Pop": ["pop", "dance pop", "electropop", "indie pop"],
    "Hip-Hop/Rap": ["hip hop", "rap", "trap"],
    "Rock": ["rock", "alt rock", "alternative", "punk", "metal", "grunge"],
    "R&B/Soul": ["r&b", "soul", "neo soul"],
    "EDM": ["edm", "house", "techno", "dubstep", "trance", "electronic"],
    "Country": ["country"],
    "Latin": ["latin", "reggaeton"],
    "K-Pop": ["k-pop"],
    "Chill/Indie": ["indie", "chill", "lo-fi", "dream pop"],
}

def pick_bucket(genres):
    all_genres = " ".join(genres).lower()
    for bucket, keywords in GENRE_BUCKETS.items():
        if any(k in all_genres for k in keywords):
            return bucket
    return "Other"


def group_songs_by_genre(tracks):
    sp = get_spotify_client()

    # unique artist ids
    artist_ids = list({t["artist_id"] for t in tracks if t.get("artist_id")})

    # Spotify allows batching artists (50 per request)
    artist_genres = {}
    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i:i+50]
        results = sp.artists(batch)["artists"]
        for a in results:
            artist_genres[a["id"]] = a.get("genres", [])

    groups = defaultdict(list)
    for t in tracks:
        genres = artist_genres.get(t.get("artist_id"), [])
        bucket = pick_bucket(genres)
        groups[bucket].append(t)

    return dict(groups)



def classify_vibe(track, features):
    """
    Basic rule-based vibe classifier.
    """

    energy = features["energy"]
    valence = features["valence"]
    tempo = features["tempo"]

    if energy > 0.7 and valence > 0.6:
        return "Hype"
    elif energy < 0.4 and valence < 0.4:
        return "Sad Chill"
    elif tempo < 100 and energy < 0.6:
        return "Mellow"
    else:
        return "Mixed"


def chunked(lst, n=50):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


def fetch_features_with_fallback(sp, track_ids):
    """
    Try batches first (smaller URL).
    If Spotify still rejects a batch, fall back to one-by-one.
    """
    features_by_id = {}

    for batch in chunked(track_ids, 50):
        try:
            feats = sp.audio_features(batch)  # <= calls /audio-features/?ids=... but shorter
            for f in feats:
                if f and f.get("id"):
                    features_by_id[f["id"]] = f
        except Exception:
            # fallback: do them one-by-one
            for tid in batch:
                try:
                    f = sp.audio_features([tid])[0]  # <= one id only
                    if f and f.get("id"):
                        features_by_id[f["id"]] = f
                except Exception:
                    continue

    return features_by_id


def group_songs_by_vibe(tracks):
    sp = get_spotify_client()  # whatever you already have (token refresh etc.)

    track_ids = [t["id"] for t in tracks if t.get("id")]
    features_by_id = fetch_features_with_fallback(sp, track_ids)

    vibe_groups = {}

    for track in tracks:
        tid = track["id"]
        features = features_by_id.get(tid)
        if not features:
            continue

        vibe = classify_vibe(track, features)
        vibe_groups.setdefault(vibe, []).append(track)

    return vibe_groups

def get_audio_features_safe(sp, track_ids):
    """
    Fallback method: fetch audio features one track at a time.
    Slower, but very reliable when the bulk endpoint errors.
    """
    features_by_id = {}

    for tid in track_ids:
        try:
            f = sp.audio_features([tid])[0]  # still calls batch, but 1 id only
            if f and f.get("id"):
                features_by_id[f["id"]] = f
        except Exception:
            # skip tracks that fail
            continue

    return features_by_id
