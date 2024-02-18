import pretty_midi
import numpy as np
from utils.chord import *
from utils.melody import *

bpm = 80

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

if __name__ == '__main__':
    output_midi = pretty_midi.PrettyMIDI()
    main_piano = pretty_midi.Instrument(program=0)
    sub_piano = pretty_midi.Instrument(program=0)

    default_scale = MajorScale('C')

    inoutro = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chord_progressions[0], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=0.2,
        bar_part=4,
        measure=(4,4),
    )
    verse = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chord_progressions[1], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=0.4,
        bar_part=8,
        measure=(4,4),
    )
    chorus = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chord_progressions[9], 4),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=0.5,
        bar_part=8,
        measure=(4,4),
    )
    bridge = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chord_progressions[-1], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        randomness=0.7,
        bar_part=8,
        measure=(4,4),
    )

    merge_part(
        part_list=[inoutro, verse, chorus, verse, chorus, bridge, chorus, inoutro],
        instrument_list=[main_piano, sub_piano],
    )

    output_midi.instruments.append(main_piano)
    output_midi.instruments.append(sub_piano)
    output_midi.write('src/test/output.mid')
