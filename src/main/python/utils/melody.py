import pretty_midi
import numpy as np
import random

bar_division = 16

pat = []
weight = [.8, .2, .4, .2] * 4

def __choice(p):
    return random.choices(
        population=[True, False],
        weights=[p, 1 - p],
        k=1
    )[0]

def make_melody_pattern(randomness=0):
    idx = list(range(bar_division))
    pattern = [__choice(weight[i]) for i in idx]
    return pattern

# testing melody pattern
if __name__ == '__main__':
    output_midi = pretty_midi.PrettyMIDI()

    main_piano = pretty_midi.Instrument(program=0)
    start_base = 0

    pat = make_melody_pattern()

    duration = 2 / bar_division

    for x in pat:
        note_number = pretty_midi.note_name_to_number('A5')
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=start_base,
            end=start_base + duration*0.75,
        )
            
        if (x == True):
            main_piano.notes.append(note)

        start_base += duration

    # for _ in range(10):
    #     print(make_melody_pattern())
    print(pat)
    output_midi.instruments.append(main_piano)
    output_midi.write('./output.mid')
