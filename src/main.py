import pretty_midi
import numpy as np
from utils.chord import *
from utils.melody import *

bpm = 80

def apply_mini_part(
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


def create_mini_part(
    output_midi,
    instruments,
    start_base,
    melody: Melody,
    chord: ChordWithPattern,
):
    global bpm

    main_instrument = instruments[0]
    sub_instrument = instruments[1]

    dur_main = (1/melody.division_count) * (240/bpm)
    dur_sub = (1/chord.division_count) * (240/bpm)

    start_base_main = apply_mini_part(
        main_instrument, start_base, dur_main, melody.notes)
    start_base_sub = apply_mini_part(
        sub_instrument, start_base, dur_sub, chord.notes)

    start_base_main = np.round(start_base_main, decimals=4)
    start_base_sub = np.round(start_base_sub, decimals=4)

    print((start_base_main, start_base_sub))
    # Note that start_base_main == start_base_sub
    if (start_base_main != start_base_sub):
        raise Exception("Length of melody and chords don't match!")
    return start_base_main

def create_part(
    scale: Scale,
    chord_pattern: ChordWithPattern,
    randomness: int,
    start_base: float,
    output_midi,
    instruments,
    bar_part: int=8,
    measure=(4,4)
):  
    bar_per_cp = chord_pattern.cp.bar_length
    
    # 기본적으로 AA'BA 형식을 따름
    melody_primary = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division_count=16
    )
    melody_diff = melody_primary.get_differ_melody(melody_randomness=0.5)
    melody_b = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division_count=16
    )

    melodies = [melody_primary, melody_diff, melody_b, melody_primary]

    for i in range(bar_part // chord_pattern.cp.bar_length):
        start_base = create_mini_part(
            output_midi=output_midi, 
            instruments=instruments, 
            start_base=start_base, 
            melody=melodies[i], 
            chord=chord_pattern
        )

    return start_base

if __name__ == '__main__':

    output_midi = pretty_midi.PrettyMIDI()
    main_piano = pretty_midi.Instrument(program=0)
    sub_piano = pretty_midi.Instrument(program=0)

    start_base = 0

    default_scale = MajorScale('C')

    verse = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chord_progressions[0], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division_count=8,
        ),
        randomness=0.2,
        start_base=start_base,
        output_midi=output_midi,
        instruments=[main_piano, sub_piano],
        bar_part=8,
        measure=(4,4),
    )

    output_midi.instruments.append(main_piano)
    output_midi.instruments.append(sub_piano)
    output_midi.write('src/test/output.mid')
