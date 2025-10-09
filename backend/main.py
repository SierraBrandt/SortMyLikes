# backend/main.py
#FastAPI app + route definitions
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from spotify_auth import sp_oauth
from spotify_utils import get_liked_tracks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/callback", response_class=HTMLResponse)
def callback(request: Request):
    code = request.query_params.get("code")
    token_info = sp_oauth.get_access_token(code)
    with open("token_info.json", "w") as f:
        json.dump(token_info, f)
    return templates.TemplateResponse("callback.html", {"request": request})

@app.get("/liked-songs", response_class=HTMLResponse)
def show_liked_songs(request: Request):
    songs = get_liked_tracks()
    return templates.TemplateResponse("liked_songs.html", {
        "request": request,
        "songs": songs
    })

@app.get("/login-redirect")
def login_redirect():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@app.get("/logout")
def logout():
    import os
    if os.path.exists("token_info.json"):
        os.remove("token_info.json")
    return RedirectResponse(url="/")