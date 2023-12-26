import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import random
from pychord import Chord
from utils.melody import *

bpm = 80

def music_generate(key, melody, start_base, main_instrument):
    global bpm

    melody_main = np.array(melody.notes)[:, 0]
    melody_dur = np.array(melody.notes)[:, 1]

    print(np.vectorize(pretty_midi.note_number_to_name)(np.array(melody_main)), melody_dur)

    dur = (1/16) * (240/bpm)

    for (m, d) in melody.notes:
        note = pretty_midi.Note(velocity=100, pitch=m, start=start_base, end=start_base + d*dur*0.75)
        main_instrument.notes.append(note)
        start_base += d*dur
    
    return start_base

def sub_generate(chord, root_pitch, start_base, sub_instrument):
    global bpm

    c = chord.components_with_pitch(root_pitch = root_pitch)
   
    dur = (1/8) * (240/bpm)
    pat = np.vectorize(pretty_midi.note_name_to_number)(np.array([c[0], c[2], c[0], c[2]]))
    pat[2] += 12

    for p in pat:
        note = pretty_midi.Note(velocity=100, pitch=p, start=start_base, end=start_base + dur)
        sub_instrument.notes.append(note)
        start_base += dur

    return start_base

output_midi = pretty_midi.PrettyMIDI()
main_piano = pretty_midi.Instrument(program=0)
sub_piano = pretty_midi.Instrument(program=0)

mscale = MajorScale('C');
melody = Melody(mscale, randomness=0.8)

start_base_main = 0
start_base_main = music_generate('C', melody, start_base_main, main_piano)
melody.differ_melody(0.2)
start_base_main = music_generate('C', melody, start_base_main, main_piano)


start_base_sub = 0
start_base_sub = sub_generate(Chord('Am'), 2, start_base_sub, sub_piano)
start_base_sub = sub_generate(Chord('F'), 2, start_base_sub, sub_piano)
start_base_sub = sub_generate(Chord('G'), 2, start_base_sub, sub_piano)
start_base_sub = sub_generate(Chord('C'), 3, start_base_sub, sub_piano)


# print(np.vectorize(pretty_midi.note_number_to_name)(np.array(melody_main)), melody_dur)
output_midi.instruments.append(main_piano)
output_midi.instruments.append(sub_piano)
output_midi.write('src/test/output.mid')
