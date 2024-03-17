import asyncio
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.generator import generator
from app.util import convert

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

app = FastAPI()

@app.post('/music')
def get_music(music_body: MusicBody):
    music_dir_path = './app/assets/music/'
    midi_file = music_dir_path + 'output.mid'
    mp3_file = music_dir_path + 'output.mp3'
    soundfont_path = music_dir_path + 'soundfont.sf2'
    
    generator.make_song(
        genre=music_body.genre,
        mood=music_body.mood,
        tempo=music_body.tempo,
        music_path=midi_file,
    )
    convert.midi_to_mp3(midi_file, soundfont_path, mp3_file)
    return FileResponse(mp3_file)
