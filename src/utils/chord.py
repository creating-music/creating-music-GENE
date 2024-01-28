from pychord import ChordProgression

chord_progressions = [
    ChordProgression(['Dm7', 'G7', 'CM7', 'CM7']),
    ChordProgression(['Dm7', 'G7', 'CM7', 'Am7']),
    ChordProgression(['Dm7', 'G7', 'CM7', 'A7']),
    ChordProgression(['FM7', 'G7', 'Em7', 'Am7']),
    ChordProgression(['FM7', 'Em7', 'Dm7', 'Em7']),
    ChordProgression(['CM7', 'G7', 'Am7', 'FM7']),
    ChordProgression(['CM7', 'Am7', 'FM7', 'G7']),
    ChordProgression(['CM7', 'FM7', 'G7', 'Am7']),
    ChordProgression(['C7', 'C7', 'F7', 'F7']),
    ChordProgression(['CM7', 'G7', 'Am7', 'Em7', 'FM7', 'CM7', 'FM7', 'G7']),
    ChordProgression(['Am7', 'FM7', 'CM7', 'G7']),
    ChordProgression(['Am7', 'FM7', 'G7', 'CM7']),
    ChordProgression(['Am7', 'Dm7', 'Em7', 'Am7']),
    ChordProgression(['Am7', 'G7', 'FM7', 'G7']),
    ChordProgression(['CM7', 'E7', 'FM7', 'Fm7']),
    ChordProgression(['CM7', 'BbM7', 'FM7', 'Fm7']),
]

class Chords:
    def __init__(
        self, 
        cp: ChordProgression, 
        bar_length: int
    ):
        self.cp = cp
        self.bar_length = bar_length