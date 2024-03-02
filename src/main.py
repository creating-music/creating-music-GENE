import pretty_midi
import numpy as np
import random
from pychord import Chord
from utils.chord import *
from utils.melody import *
from utils.util import *

# bpm = 80

class NoteWrapper:
    def __init__(self, notes, division):
        self.notes = notes
        self.division = division

    def __str__(self):
        return f'notes: {self.notes}\ndivision: {self.division}'

def apply_midi(
    instrument,
    start_base,
    duration,
    notes
):
    for (n, d) in notes:
        note = pretty_midi.Note(
            velocity=100, 
            pitch=n,
            start=start_base, 
            end=start_base + d*duration
        )
        instrument.notes.append(note)
        start_base += d*duration

    return start_base

def create_part(
    scale: Scale,
    chord_pattern: ChordWithPattern,
    randomness: int,
    bar_part: int=8,
    measure=(4,4)
):  
    bar_per_cp = chord_pattern.cp.bar_length

    if (bar_part < bar_per_cp):
        raise Exception('Song length is smaller than chord length!')
   
    melody_primary = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division=16
    )
    melody_diff = melody_primary.get_differ_melody(melody_randomness=0.5)
    melody_b = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division=16
    )

    # 기본적으로 AA'BA 형식을 따름
    if (bar_part == bar_per_cp):
        melodies = [melody_primary]
    elif (bar_part == 2 * bar_per_cp):
        melodies = [melody_primary, melody_diff]
    elif (bar_part == 4 * bar_per_cp):
        melodies = [melody_primary, melody_diff, melody_b, melody_primary]
    elif (bar_part == 8 * bar_per_cp):
        melodies = [melody_primary, melody_diff, melody_b, melody_primary] * 2
    else:
        raise Exception('Unsupported bar length.')

    melody_note_total = []
    for melody in melodies:
        melody_note_total.extend(melody.notes)
    melody_wrapper = NoteWrapper(melody_note_total, melody_primary.division)

    chords = [chord_pattern] * (bar_part // bar_per_cp)
    chord_note_total = []
    for chord in chords:
        chord_note_total.extend(chord.notes)
    chord_wrapper = NoteWrapper(chord_note_total, chord_pattern.division)

    return [melody_wrapper, chord_wrapper]

def merge_part(
    part_list: list[list[NoteWrapper]],
    instrument_list: list[pretty_midi.Instrument],
    bpm: int,
):
    start_base = 0

    for part in part_list:
        if len(part) != len(instrument_list):
            raise Exception(f'Must contain {len(instrument_list)} instruments.')

        start_base_each = 0
        for (note_wrapper, instrument) in zip(part, instrument_list):
            duration = (1/note_wrapper.division) * (240/bpm)
            start_base_each = apply_midi(instrument, start_base, duration, note_wrapper.notes)
            start_base_each = np.round(start_base_each, decimals=4)

        start_base = start_base_each

def make_song(
    genre: str,
    mood: str,
    bpm: int | None=None,
    max_randomness: int=0.7,
):
    if genre not in ['newage', 'retro']:
        raise Exception('Unsupported genre.')

    if mood not in ['happy', 'sad', 'grand']:
        raise Exception('Unsupported mood.')

    quant_size = 0.1
    limitations = {
        'newage': {
            'bpm': set(range(60, 120 + 1)),
            'randomness': set(np.arange(0.2, 0.6, quant_size)),
        },
        'retro': {
            'bpm': set(range(80, 160 + 1)),
            'randomness': set(np.arange(0.2, 0.9, quant_size)),
        },
        'happy': {
            'bpm': set(range(80, 160 + 1)),
            'randomness': set(np.arange(0.1, 0.9, quant_size)),
        },
        'sad': {
            'bpm': set(range(60, 100 + 1)),
            'randomness': set(np.arange(0.1, 0.8, quant_size)),
        },
        'grand': {
            'bpm': set(range(60, 90 + 1)),
            'randomness': set(np.arange(0.1, 0.8, quant_size)),
        },
    }

    if bpm is None:
        # 장르와 무드에 따라 bpm 설정
        bpm_list = list(limitations[genre]['bpm'].intersection(limitations[mood]['bpm']))
        bpm = random.choice(bpm_list)

    randomness_list = list(limitations[genre]['randomness'].intersection(limitations[mood]['randomness']))

    rand_limit_high = min(max_randomness, randomness_list[-1])
    randomness_list = np.linspace(randomness_list[0], rand_limit_high, 50)

    randomness_selection = sorted([
        random.choice(randomness_list),
        random.choice(randomness_list),
        random.choice(randomness_list),
        random.choice(randomness_list),
    ])

    print(randomness_selection, bpm)

    instruments = {
        'newage': [pretty_midi.Instrument(program=0), pretty_midi.Instrument(program=0)],
        'retro': [pretty_midi.Instrument(program=80), pretty_midi.Instrument(program=81)],
    }

    # song making start
    output_midi = pretty_midi.PrettyMIDI()
    [main_instrument, sub_instrumnet] = instruments[genre]

    deviation = random.randint(0, 11)
    default_scale = MajorScale(get_transposed_root('C', deviation))

    chords_selection = [get_transposed_cp(random.choice(chord_progressions), deviation) for _ in range(4)]

    inoutro = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[0], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=randomness_selection[0],
        bar_part=4,
        measure=(4, 4),
    )
    verse = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[1], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=randomness_selection[1],
        bar_part=8,
        measure=(4, 4),
    )
    chorus = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[2], len(chords_selection[2]) // 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=randomness_selection[2],
        bar_part=8,
        measure=(4, 4),
    )
    bridge = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[3], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=randomness_selection[3],
        bar_part=8,
        measure=(4, 4),
    )

    merge_part(
        part_list=[inoutro, verse, chorus, verse, chorus, bridge, chorus, inoutro],
        instrument_list=[main_instrument, sub_instrumnet],
        bpm=bpm,
    )

    output_midi.instruments.append(main_instrument)
    output_midi.instruments.append(sub_instrumnet)
    output_midi.write('src/test/output.mid')

if __name__ == '__main__':
    make_song(
        genre='newage',
        mood='happy',
    )
