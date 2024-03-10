import asyncio
from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from generator import generator

app = FastAPI()

@app.get('/')
def read_root():
    return {'hello': 'world'}


@app.get('/music')
def get_music():
    music_path = './assets/music/output.mid'
    generator.make_song(
        genre='retro',
        mood='happy',
        music_path=music_path,
    )
    return FileResponse(music_path)
