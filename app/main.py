import asyncio
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from app.generator import generator
from app.util import convert

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

app = FastAPI()

@app.post('/music', status_code=200)
def get_music(music_body: MusicBody):
    music_dir_path = './app/assets/music/'
    midi_file = music_dir_path + 'output.mid'
    mp3_file = music_dir_path + 'output.mp3'
    soundfont_path = music_dir_path + 'soundfont.sf2'

    header = {
        'isSuccess': 'true',
        'code': '200',
        'message': '',
    }

    try:
        generator.make_song(
            genre=music_body.genre,
            mood=music_body.mood,
            tempo=music_body.tempo,
            music_path=midi_file,
        )
    except:
        header['isSuccess'] = 'false'
        header['code'] = '500'
        header['message'] = 'music generation fail'

        # 비어있는 파일을 반환
        return JSONResponse('', headers=header)
    
    try:
        convert.midi_to_mp3(midi_file, soundfont_path, mp3_file)
    except:
        header['isSuccess'] = 'false'
        header['code'] = '500'
        header['message'] = 'music rendering fail'

        # 비어있는 파일을 반환
        return JSONResponse('', headers=header)

    header['message'] = 'music generation success'

    return FileResponse(mp3_file, headers=header)
