import asyncio
from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.generator import generator

app = FastAPI()

@app.get('/')
def read_root():
    return {'hello': 'world'}


@app.get('/music')
def get_music():
    music_path = './app/assets/music/output.mid'
    generator.make_song(
        genre='retro',
        mood='happy',
        tempo='slow',
        music_path=music_path,
    )
    return FileResponse(music_path)
