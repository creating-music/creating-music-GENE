import os
from pydub import AudioSegment

def midi_to_mp3(midi_file, soundfont, mp3_file):
    # Convert MIDI to WAV using fluidsynth
    wav_file = mp3_file.replace('.mp3', '.wav')
    print(wav_file)
    os.system(f'fluidsynth -ni {soundfont} {midi_file} -F {wav_file} -r 44100')
    
    # Convert WAV to MP3 using pydub
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format='mp3')
    # Remove temporary WAV file
    os.remove(wav_file)
