from pychord import Chord, ChordProgression

def divide_chunk(list_dividend, division_size):
    def __divide_chunk(l, n):
        for i in range(0, len(l), n):
            yield l[i : i+n]

    return list(__divide_chunk(list_dividend, division_size))

def divide_chunk_into(list_dividend, num):
    division_size = len(list_dividend) // num
    division_res = len(list_dividend) % num

    if (division_res != 0):
        raise Exception('Not equally divisible.')

    return divide_chunk(list_dividend, division_size)

def get_transposed_root(root: str, amount: int) -> str:
    __notes_with_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    __notes_with_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

    idx = 0
    is_sharp = True
    if (root in __notes_with_sharp):
        idx = __notes_with_sharp.index(root)
        is_sharp = True
    else:
        idx = __notes_with_flat.index(root)
        is_sharp = False
    
    idx = idx + amount
    idx = idx % 12

    scale = __notes_with_sharp if is_sharp else __notes_with_flat
    return scale[idx]

def get_transposed_chord(chord: Chord, amount: int):
    c = Chord(chord.chord)
    c.transpose(amount)
    return c

def get_transposed_cp(cp: ChordProgression, amount: int):
    c = ChordProgression(cp.chords)
    c.transpose(amount)
    return c
