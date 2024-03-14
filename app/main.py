import asyncio
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.generator import generator

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

app = FastAPI()

@app.post('/music')
def get_music(music_body: MusicBody):
    music_path = './app/assets/music/output.mid'
    generator.make_song(
        genre=music_body.genre,
        mood=music_body.mood,
        tempo=music_body.tempo,
        music_path=music_path,
    )
    return FileResponse(music_path)
