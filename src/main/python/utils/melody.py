import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import random

'''
Pattern of melody.

Pattern is binary array. ex) [True, False, False, ...]
The melody will be played only for True value.
''' 
class MelodyPattern:
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
        pretty_midi.note_name_to_number('E3'),
        pretty_midi.note_name_to_number('E6') + 1
    )

    def __init__(
            self, 
            scale,
            randomness,
            bar_length=1,
            division_count=16,
            measure=(4,4),
            pattern=None, 
            notes=[], 
            velocity=[]
        ):
        super().__init__(randomness, bar_length, division_count, measure)
        self.scale = scale
        self.notes = notes
        self.velocity = velocity
        self.limit = list(set(Melody.limit).intersection(scale.scale))

        # randomness와 pattern을 동시에 넘겨주면, randomness는 pattern에 영향을 주지 않음.
        # 즉, 주어진 pattern으로 고정.
        if (pattern != None):
            self.pattern = pattern
        
        if (notes == []):
            self.build_melody()

        if (velocity == []):
            self.build_velocity()

    @staticmethod
    def _calc_next_note(curr_note_index, randomness, max_limit):
        while True:
            next_dist = np.random.normal(curr_note_index, randomness+0.1)
            next_note_index = np.floor(next_dist).astype(int) 
            
            if next_note_index in range(max_limit):
                return next_note_index

    def build_melody(self):
        limit_len = len(self.limit)
        note_index = 0
        note_len = 1
        is_first_note = True
        for i in self.pattern:
            if (i == 0):
                note_len += 1
                continue
               
            # only for the i == 1 case
            if (is_first_note):
                is_first_note = False
                note_index = random.choice(range(limit_len))
                continue
           
            # 전의 note를 append.
            self.notes.append([
                self.limit[note_index],
                note_len
            ]) 

            note_len = 1
            note_index = Melody._calc_next_note(
                note_index,
                self.randomness,
                limit_len
            )
        
        # 마지막 note 까지 append
        self.notes.append([
            self.limit[note_index],
            note_len
        ]) 
            
    def build_velocity(self):
        pass

class Scale:
    def __init__(
            self,
            root,
        ):
        self.root = root
        self.scale = set()

    def build_scale(self):
        pass

class MajorScale(Scale):
    def __init__(
            self,
            root
            ):
        super().__init__(root)
        self._build_scale()

    def _build_scale(self):
        # A4 = 440Hz. 높은 음자리표에 맞춤.
        OCTAVE = 12
        root_as_number = pretty_midi.note_name_to_number(f'{self.root}4')
        weight = np.arange(-4, 5) * OCTAVE
        main_scale = np.array([0, 2, 4, 5, 7, 9, 11])
        scale = []
        for w in weight:
            scale.extend(main_scale + root_as_number - w)
        self.scale = set(scale)

if __name__ == '__main__':
    mscale = MajorScale('C');
    melody = Melody(MajorScale('C'), 1)

    melody_main = np.array(melody.notes)[:, 0]
    melody_dur = np.array(melody.notes)[:, 1]
    p = melody.pattern

    output_midi = pretty_midi.PrettyMIDI()
    main_piano = pretty_midi.Instrument(program=0)

    start_base = 0
    for (m, d) in zip(melody_main, melody_dur):
        note = pretty_midi.Note(velocity=100, pitch=m, start=start_base, end=start_base + d/4 - 0.25/4)
        main_piano.notes.append(note)
        start_base += d/4

    print(np.vectorize(pretty_midi.note_number_to_name)(np.array(melody_main)), melody_dur)
    output_midi.instruments.append(main_piano)
    output_midi.write('output.mid')
