import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import random
from pychord import Chord, ChordProgression
from typing import Tuple
from .chord import Chords


class Scale:
    __notes_with_sharp = ['A', 'A#', 'B', 'C',
                          'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    __notes_with_flat = ['A', 'Bb', 'B', 'C',
                         'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    OCTAVE = 12

    def __init__(
        self,
        root,
        scale,
        mode
    ):
        self.root = root                    # 근음. ex) 'C'
        # 스케일의 음 간격. ex) [0, 2, 4, 5, 7, 9, 11]
        self.default_scale = scale
        self.scale = None                   # 실제 스케일의 음.
        self.mode = mode                    # 몇 번째 모드인지. 1 이면 원래 스케일과 동일.
        self.scale_name = None              # 스케일의 이름 (Major, Minor...)
        self.build_scale(scale)

    @staticmethod
    def estimate_scale(chord: Chord):
        quality_string = str(chord.quality)
        if (quality_string.isdigit()):
            return MajorScale(chord.root, 5)        # Dominant 7
        if ('m' in quality_string and 'b5' in quality_string):
            return MajorScale(chord.root, 7)        # Half-diminished
        if ('mM' in quality_string):
            return MelodicMinorScale(chord.root)
        if (quality_string == '' or 'M' in quality_string):
            return MajorScale(chord.root)
        if ('m' in quality_string):
            return MajorScale(chord.root, 6)        # Natural minor
        if ('dim' in quality_string):
            return DiminishedScale(chord.root)
        return AlteredScale(chord.root)

    def build_scale(self, scale):
        # A4 = 440Hz. 높은 음자리표에 맞춤.

        if (self.mode != 1):
            self.root = self.unmoded_root()

        root_as_number = pretty_midi.note_name_to_number(f'{self.root}4')
        weight = np.arange(-3, 5) * Scale.OCTAVE
        main_scale = np.array(scale)
        result_scale = []
        for w in weight:
            result_scale.extend(main_scale + root_as_number - w)
        self.scale = set(result_scale)

    def has_note(self, note_name):
        '''
        스케일에 해당 음이 있는지 확인.
        '''

        if (note_name in Scale.__notes_with_sharp):
            idx = Scale.__notes_with_sharp.index(note_name)
        else:
            idx = Scale.__notes_with_flat.index(note_name)

        if (self.root in Scale.__notes_with_sharp):
            root_idx = Scale.__notes_with_sharp.index(self.root)
        else:
            root_idx = Scale.__notes_with_flat.index(self.root)

        diff = idx - root_idx
        if (diff < 0):
            diff += Scale.OCTAVE

        return diff in self.default_scale

    def has_chord(self, chord: Chord):
        '''
        주어진 코드가 스케일 내에 있는지 확인.
        '''

        res = True
        for note in chord.components():
            res = res and self.has_note(note)

        return res

    def unmoded_root(self):
        '''
        모드에 의해 변경되기 전의 근음 반환.
        ex) Major scale에서 주어진 root가 A이고, mode가 6이면 C를 반환.
        '''

        if (self.root in Scale.__notes_with_sharp):
            idx = Scale.__notes_with_sharp.index(self.root)
            is_sharp = True
        else:
            idx = Scale.__notes_with_flat.index(self.root)
            is_sharp = False

        offset = self.default_scale[self.mode - 1]
        idx = (idx - offset) % Scale.OCTAVE

        notes = Scale.__notes_with_sharp if is_sharp else Scale.__notes_with_flat
        return notes[idx]

    def print_scale(self):
        print(f'{self.root} {self.scale_name}')


class MajorScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 5, 7, 9, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Major'

    @property
    def moded_scale_name(self):
        scale_name = ['Ionian', 'Dorian', 'Phrygian',
                      'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
        return scale_name[self.mode - 1]


class MelodicMinorScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 3, 5, 7, 9, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Melodic minor'


class PentatonicScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 7, 9]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Pentatonic'


class BluesScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 3, 5, 6, 7, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Blues'


class WholeToneScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 6, 8, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Whole tone'


class ChromaticScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Chromatic'


class DiminishedScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 3, 4, 6, 7, 9, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Diminished'


class AlteredScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 3, 4, 6, 8, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Altered'


class MelodyPattern:
    '''
    Pattern of melody.

    Pattern is binary array. ex) [True, False, False, ...]
    The melody will be played only for True value.
    '''

    def __init__(
        self,
        randomness,
        bar_length=1,
        division_count=16,
        measure=(4, 4)
    ):

        self.randomness = randomness            # 무작위도
        self.bar_length = bar_length            # 마디 개수
        self.division_count = division_count    # 한 마디를 몇 개로 나눌건지
        self.measure = measure                  # 박자

        self._make_probability_distribution()    # pattern을 생성할 확률분포
        self.build_pattern()                     # 멜로디 패턴

        # note가 두 개 이하면 다시 생성.
        while sum(self.pattern) <= 2:
            self.build_pattern()

    def __repr__(self):
        return self.pattern

    def __str__(self):
        return str(self.pattern)

    # 주어진 확률에 따라 1 또는 0 선택.
    @staticmethod
    def _choice(p):
        return random.choices(
            population=[1, 0],
            weights=[p, 1 - p],
            k=1
        )[0]

    # 패턴의 확률분포를 만듦.
    # 큰 randomness는 더욱 분산이 큰 분포를 만듦 = 높은 엔트로피.
    def _make_probability_distribution(self):
        depth = np.log2(self.division_count).astype(np.uint8) - 1
        weights = np.zeros(depth)

        r = self.randomness
        primary = -0.5*(r - 2)

        def h(x, a): return x/a

        # 정박이 아닌 박의 확률을 구하기 위해 interpolate.
        # somthing magical happens (?)
        weights[0] = primary

        for i in range(depth - 1):
            weights[i+1] = (1-h(r, 2**i))*(1-primary) + h(r, 2**i)*primary

        pd = np.zeros(self.bar_length * self.division_count)

        for i in reversed(range(depth)):
            step = (self.division_count // self.measure[1]) // 2**i
            pd[::step] = weights[i]

        self._pd = pd

    # 확률분포에 따라 패턴 생성.
    def build_pattern(self):
        pattern = [MelodyPattern._choice(p) for p in list(self._pd)]
        self.pattern = pattern


class Melody(MelodyPattern):
    # 멜로디가 올라갈 / 내려갈 수 있는 한계.
    limit = range(
        pretty_midi.note_name_to_number('E4'),
        pretty_midi.note_name_to_number('E6') + 1
    )
    __RANDOM_WEIGHT = 3

    def __init__(
        self,
        scale: Scale,
        randomness: int,
        chord_progression: Chords,
        bar_length=1,
        division_count=16,
        measure: tuple[int, int] = (4, 4),
        pattern: MelodyPattern = None,
        notes: list[int] = None,
        velocity: list[int] = None
    ):
        super().__init__(randomness, bar_length, division_count, measure)
        self.scale: Scale = scale
        self.notes: list[int] = notes
        self.velocity: list[int] = velocity
        self.usable_notes = list(set(Melody.limit).intersection(scale.scale))
        self.chord_progression = chord_progression
        self.start_chord = Chord('CM7')

        # randomness와 pattern을 동시에 넘겨주면,f randomness는 pattern에 영향을 주지 않음.
        # 즉, 주어진 pattern으로 고정.
        if (pattern is not None):
            self.pattern = pattern

        if (notes is None):
            self.notes = []
            self.build_melody()

        if (velocity is None):
            self.velocity = []
            self.build_velocity()

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

    @staticmethod
    def _calc_next_note(curr_note_number, usable_notes, randomness):
        '''
            return next_note's number
        '''
        curr_note_index = find_nearest(usable_notes, curr_note_number)[0]

        while True:
            next_dist = np.random.normal(
                curr_note_index, Melody.__RANDOM_WEIGHT*randomness+0.1)
            next_note_index = np.floor(next_dist).astype(int)

            if (0 <= next_note_index < len(usable_notes)):
                return usable_notes[next_note_index]

    @staticmethod
    def _choose_from_chord(chord: Chord, curr_note, randomness=0):
        '''
            return next_note's number
        '''

        chord_notes_number = []
        for c in chord.components():
            chord_notes_number.append(pretty_midi.note_name_to_number(f'{c}4'))
        weight = np.arange(-3, 5) * Scale.OCTAVE
        chord_notes_number = np.array(chord_notes_number)
        result_chord_notes = []
        for w in weight:
            result_chord_notes.extend(chord_notes_number - w)
        chord_notes_number = list(
            set(result_chord_notes).intersection(Melody.limit))

        if (curr_note == 0):
            return random.choice(chord_notes_number)

        pivot_idx = find_nearest(chord_notes_number, curr_note)[0]

        while True:
            next_dist = np.random.normal(
                pivot_idx, Melody.__RANDOM_WEIGHT*randomness+0.1)
            next_note_idx = np.floor(next_dist).astype(int)

            if (0 <= next_note_idx < len(chord_notes_number)):
                return chord_notes_number[next_note_idx]

    def build_melody(self):
        # 코드 진행을 마디 크기로 분할
        cp_bar = self.chord_progression.bar_length
        cp_len = len(self.chord_progression.cp)
        chord_num_for_each_bar = cp_len // cp_bar

        cps: list[ChordProgression] = []
        _chords: list[Chord] = []
        for i in range(cp_len):
            _chords.append(self.chord_progression.cp[i])
            if ((i+1) % chord_num_for_each_bar == 0):
                cps.append(ChordProgression(_chords))
                _chords = []

        notes = []
        for cp in cps:
            notes.extend(self._make_bar(cp))

        self.notes = notes

    def _make_bar(self, cp: ChordProgression):
        '''
        한 마디에 해당하는 멜로디를 만듦
        '''
        cp_len = len(cp)
        note_num_for_each_chord = self.division_count // cp_len

        scale = self.scale

        note_number = 0
        note_len = 1
        notes = []

        usable_notes = self.usable_notes
        for (idx, p) in enumerate(self.pattern):

            nth_chord = idx // note_num_for_each_chord
            is_first_note_of_chord = idx % note_num_for_each_chord == 0
            curr_chord = cp[nth_chord]

            if (is_first_note_of_chord):
                # 해당 코드의 첫 음 처리
                if (self.scale.has_chord(curr_chord)):
                    scale = self.scale
                else:
                    scale = Scale.estimate_scale(cp[nth_chord])
                usable_notes = list(scale.scale.intersection(Melody.limit))

            if (p == 0):
                note_len += 1
                continue

            if (is_first_note_of_chord):
                note_number = Melody._choose_from_chord(
                    curr_chord, note_number, self.randomness)
                continue

            # 이전의 note를 append.
            notes.append([
                note_number,
                note_len
            ])

            note_len = 1
            note_number = Melody._calc_next_note(
                note_number,
                usable_notes,
                self.randomness,
            )

        # 마지막 note 까지 append
        notes.append([
            note_number,
            note_len
        ])

        return notes

    def build_velocity(self):
        pass

    # 주어진 melody, pattern randomness에 따라 음을 약간 변화시킨다.
    # melody_randomness 의 확률로 원래의 음을 살림.
    def differ_melody(self, melody_randomness, pattern_randomness=0):
        limit_len = len(self.usable_notes)
        res_melody = []
        for (mel, dur) in self.notes:
            if (random.uniform(0, 1) <= melody_randomness):
                res_melody.append([mel, dur])
            else:
                # 현재 멜로디와 가장 가까운 음을 찾는다.
                curr_mel_index = self.usable_notes.index(mel)
                next_mel_index = Melody._calc_next_note(
                    curr_mel_index, self.randomness, limit_len)
                next_mel = self.usable_notes[next_mel_index]
                res_melody.append([next_mel, dur])

        self.notes = res_melody


def find_nearest(array, value):
    array = np.array(array)
    idx = (np.abs(array - value)).argmin()
    return (idx, array[idx])


def printMelody(melody):
    melody_main = np.array(melody.notes)[:, 0]
    melody_dur = np.array(melody.notes)[:, 1]

    print(np.vectorize(pretty_midi.note_number_to_name)
          (np.array(melody_main)), melody_dur)


if __name__ == '__main__':
    mscale = MajorScale('C')
    melody = Melody(mscale, randomness=0.5)
    melody_2 = Melody(mscale, randomness=0.8)

    printMelody(melody)
    printMelody(melody_2)
