from xml.dom.pulldom import default_bufsize
from pychord import Chord, ChordProgression
import pretty_midi
import numpy as np

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
        self.bar_length: int = bar_length
        self.chord_nums: int = len(cp)


class Pattern:
    def __init__(
        self,
        pattern: list[int],
        measure: tuple[int, int]
    ) -> None:
        self.pattern = pattern
        self.measure = measure
        self.length = len(pattern)


class ArpeggioPattern(Pattern):
    def __init__(
        self,
        measure=(4, 4),
        method='one-five'
    ):
        # Only for 4/4 measure.
        default_patterns = {
            'one-five': [0, 2, 0 + 12, 2],
            'one-five-seven': [0, 2, 3, 2],
            'one-three': [0, 1, 0 + 12, 1],
            'one-three-seven': [0, 1, 3, 1],
            'arpeggio': [0, 1, 2, 3]
        }
        if (method not in default_patterns.keys()):
            return

        super().__init__(default_patterns[method], measure)


class ChordWithPattern:
    def __init__(
        self,
        cp: Chords,
        pattern: Pattern,
        division_count=8,
    ):
        self.cp = cp
        self.division_count = division_count
        self.pattern = pattern
        self.build_chord()

    def __str__(self, with_name=False):
        if (not with_name):
            return str(self.notes)

        notes = np.array(self.notes)
        note_numbers = notes[:, 0]
        note_durations = notes[:, 1]

        res = []
        for (name, duration) in zip(note_numbers, note_durations):
            res.append([pretty_midi.note_number_to_name(name), duration])

        return str(res)

    def build_chord(self):
        bar_length = self.cp.bar_length
        pattern_nums = (
            bar_length * self.division_count) // self.pattern.length
        chord_pattern = self.pattern.pattern * pattern_nums

        for (i, pat) in enumerate(chord_pattern):
            default_pitch = 3
            curr_chord: Chord = self.cp.cp[i //
                                           (len(chord_pattern) // self.cp.chord_nums)]
            chord_component = curr_chord.components_with_pitch(default_pitch)

            note_pitch = pat // 12
            note_order = (pat % 12) % len(chord_component)

            note = pretty_midi.note_name_to_number(chord_component[note_order])
            note += note_pitch * 12

            chord_pattern[i] = [note, 1]

        self.notes = chord_pattern
