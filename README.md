# SortMyLikes

A FastAPI web app that authenticates users with Spotify OAuth and groups their liked songs into mock playlists based on genre.

## Tech Stack
- FastAPI
- Spotipy (Spotify Web API)
- OAuth 2.0
- Jinja2
- Python

## Features
- Spotify login via OAuth
- Fetch liked songs
- Group songs into genre-based mock playlists
- Render grouped results dynamically

## Setup

1. Clone the repo
2. Create a Spotify Developer App
3. Add redirect URI:
   http://127.0.0.1:8000/callback
4. Create a `.env` file using `.env.example`
5. Install dependencies:
   pip install -r requirements.txt
6. Run:
   python -m uvicorn main:app --reload
