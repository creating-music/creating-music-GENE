from tracemalloc import start
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import random
from pychord import Chord
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
            end=start_base + d*duration*0.75
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

    # Note that start_base_main == start_base_sub
    if (start_base_main != start_base_sub):
        raise Exception("Length of melody and chords don't match!")
    return start_base_main


output_midi = pretty_midi.PrettyMIDI()
main_piano = pretty_midi.Instrument(program=0)
sub_piano = pretty_midi.Instrument(program=0)

start_base = 0

default_scale = MajorScale('C')
c = ChordWithPattern(
    cp=Chords(chord_progressions[1], 2),
    pattern=ArpeggioPattern(pat_method='one-three-seven', dur_method='sustain'),
    division_count=8
)
m = Melody(
    scale=default_scale,
    randomness=1,
    chord_progression=c.cp,
    measure=(4, 4),
    division_count=16
)

c2 = ChordWithPattern(
    cp=Chords(chord_progressions[2], 2),
    pattern=ArpeggioPattern(pat_method='one-three-seven', dur_method='sustain'),
    division_count=8
)
m2 = Melody(
    scale=default_scale,
    randomness=1,
    chord_progression=c2.cp,
    pattern=m.pattern
)

start_base = create_mini_part(
    output_midi=output_midi,
    instruments=[main_piano, sub_piano],
    start_base=start_base,
    melody=m,
    chord=c,
)
start_base = create_mini_part(
    output_midi=output_midi,
    instruments=[main_piano, sub_piano],
    start_base=start_base,
    melody=m2,
    chord=c2,
)

output_midi.instruments.append(main_piano)
output_midi.instruments.append(sub_piano)
output_midi.write('src/test/output.mid')