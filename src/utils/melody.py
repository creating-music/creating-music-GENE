import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import random
from pychord import Chord
from typing import Tuple


class Scale:
    __notes_with_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    __notes_with_flat  = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    __OCTAVE = 12

    def __init__(
            self,
            root,
            scale
        ):
        self.root = root                    # 근음. ex) 'C'
        self.default_scale = scale          # 스케일의 음 간격. ex) [0, 2, 4, 5, 7, 9, 11]
        self.scale = None                   # 실제 스케일의 음. 
        self.__mode = 1                     # 몇 번째 모드인지.
        self.build_scale(scale)

    def build_scale(self, scale):
        # A4 = 440Hz. 높은 음자리표에 맞춤.
        
        root_as_number = pretty_midi.note_name_to_number(f'{self.root}4')
        weight = np.arange(-4, 5) * Scale.__OCTAVE
        main_scale = np.array(scale)
        result_scale = []
        for w in weight:
            result_scale.extend(main_scale + root_as_number - w)
        self.scale = set(result_scale)

    def has_note(self, note_name):
        '''
        스케일에 해당 음이 있는지 확인.
        '''

        Scale.__OCTAVE = 12

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
            diff + Scale.__OCTAVE

        return diff in self.default_scale
        
    def has_chord(self, chord: Chord):
        '''
        주어진 코드가 스케일 내에 있는지 확인.
        '''
        
        res = True
        for note in chord.components():
            res = res and self.has_note(note)
            
        return res

    def modedRoot(self, sharpOrFlat='sharp'):
        '''
        모드에 의해 변경된 근음 반환.
        '''

        if (sharpOrFlat not in ['sharp', 'flat']): 
            return

        if (self.root in Scale.__notes_with_sharp):
            idx = Scale.__notes_with_sharp.index(self.root)
        else:
            idx = Scale.__notes_with_flat.index(self.root)
        
        offset = self.default_scale[self.__mode]
        idx = (offset + idx) % Scale.__OCTAVE
        
        notes = Scale.__notes_with_sharp if (sharpOrFlat == 'sharp') else Scale.__notes_with_flat
        return notes[idx]

    @property 
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        # Normalize mode
        mode = ((mode - 1) % len(self.default_scale)) + 1

class MajorScale(Scale):
    def __init__(
            self,
            root
            ):
        default_scale = [0, 2, 4, 5, 7, 9, 11]
        super().__init__(root, default_scale)

    def modedScaleName(self):
        scale_name = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
        return scale_name[self.mode]
        
class MelodicMinorScale(Scale):
    def __init__(
            self,
            root
            ):
        default_scale = [0, 2, 3, 5, 7, 9, 11]
        super().__init__(root, default_scale)

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
            measure=(4,4)
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

        h = lambda x, a: x/a
      
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

    def __init__(
            self, 
            scale: Scale,
            randomness: int,
            start_chord: Chord=None,
            bar_length=1,
            division_count=16,
            measure: tuple[int, int]=(4,4),
            pattern: MelodyPattern=None, 
            notes: list[int]=None, 
            velocity: list[int]=None
        ):
        super().__init__(randomness, bar_length, division_count, measure)
        self.scale: Scale = scale
        self.notes: list[int] = notes
        self.velocity: list[int] = velocity
        self.usable_notes = list(set(Melody.limit).intersection(scale.scale))
        self.start_chord = start_chord

        # randomness와 pattern을 동시에 넘겨주면, randomness는 pattern에 영향을 주지 않음.
        # 즉, 주어진 pattern으로 고정.
        if (pattern is not None):
            self.pattern = pattern
        
        if (notes is None):
            self.notes = []
            self.build_melody()

        if (velocity is None):
            self.velocity = []
            self.build_velocity()

    @staticmethod
    def _calc_next_note(curr_note_index, randomness, max_limit):
        while True:
            next_dist = np.random.normal(curr_note_index, 2*randomness+0.1)
            next_note_index = np.floor(next_dist).astype(int) 
            
            if next_note_index in range(max_limit):
                return next_note_index

    @staticmethod
    def _choose_from_chord(chord: Chord):
        min_range_num = int(pretty_midi.note_number_to_name(Melody.limit[0])[-1])
        max_range_num = int(pretty_midi.note_number_to_name(Melody.limit[-1])[-1])
        chord_octave_range = range(min_range_num, max_range_num + 1)


        while True:
            note_name = random.choice(chord.components()) + str(random.choice(chord_octave_range))
            note_number = pretty_midi.note_name_to_number(note_name)

            if (note_number in Melody.limit):
                return note_number

    def build_melody(self):
        limit_len = len(self.usable_notes)
        start_chord = self.start_chord
        note_index = 0
        note_number = 0
        note_len = 1

        is_first_note = True
        for i in self.pattern:
            if (i == 0):
                note_len += 1
                continue
               
            if (is_first_note and start_chord is not None):
                weight = 0.5 if self.scale.has_chord(start_chord) else 1

                # 코드가 스케일에 맞지 않으면 최대한 코드를 중시.
                # 코드의 음들로 첫 음 결정.
                if (random.uniform(0, 1) <= weight):
                    is_first_note = False
                    note_number = Melody._choose_from_chord(start_chord)
                    continue
                else:
                    pass    # fall through

            # 첫 음 처리. --> 주어진 코드를 바탕으로 가중치 설정.
            # 만약 코드가 주어지지 않았다면 무작위로 설정.
            if (is_first_note):
                is_first_note = False

                note_index = random.choice(range(limit_len))
                note_number = self.usable_notes[note_index]
                continue

            
            # 이전의 note를 append.
            self.notes.append([
                note_number,
                note_len
            ]) 

            note_len = 1
            note_index = Melody._calc_next_note(
                note_index,
                self.randomness,
                limit_len
            )
            note_number = self.usable_notes[note_index]
        
        # 마지막 note 까지 append
        self.notes.append([
            note_number,
            note_len
        ]) 

        print(self.notes)
            
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
                next_mel_index = Melody._calc_next_note(curr_mel_index, self.randomness, limit_len)
                next_mel = self.usable_notes[next_mel_index]
                res_melody.append([next_mel, dur])

        self.notes = res_melody


def printMelody(melody):
    melody_main = np.array(melody.notes)[:, 0]
    melody_dur = np.array(melody.notes)[:, 1]

    print(np.vectorize(pretty_midi.note_number_to_name)(np.array(melody_main)), melody_dur)

if __name__ == '__main__':
    mscale = MajorScale('C');
    melody = Melody(mscale, randomness=0.5)
    melody_2 = Melody(mscale, randomness=0.8)

    # melody_main = np.array(melody.notes)[:, 0]
    # melody_dur = np.array(melody.notes)[:, 1]
    # p = melody.pattern

    # output_midi = pretty_midi.PrettyMIDI()
    # main_piano = pretty_midi.Instrument(program=0)

    # start_base = 0
    # for (m, d) in zip(melody_main, melody_dur):
    #     note = pretty_midi.Note(velocity=100, pitch=m, start=start_base, end=start_base + d/4 - 0.25/4)
    #     main_piano.notes.append(note)
    #     start_base += d/4

    # print(np.vectorize(pretty_midi.note_number_to_name)(np.array(melody_main)), melody_dur)
    # output_midi.instruments.append(main_piano)
    # output_midi.write('src/test/output.mid')

    printMelody(melody)
    printMelody(melody_2)
