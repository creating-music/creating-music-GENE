import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
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

        self._pd = self._make_probability_distribution()    # pattern을 생성할 확률분포
        self.pattern = self._build_pattern()                # 멜로디 패턴

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
      
        # 정박이 아닌 박에 대해 interpolation 진행.
        # somthing magical happens (?)
        weights[0] = primary

        for i in range(depth - 1):
            weights[i+1] = (1-h(r, 2**i))*(1-primary) + h(r, 2**i)*primary

        pd = np.zeros(self.bar_length * self.division_count)

        for i in reversed(range(depth)):
            step = self.measure[0] // 2**i
            pd[::step] = weights[i]

        return pd
       
    # 확률분포에 따라 패턴 생성.
    def _build_pattern(self):
        pattern = [MelodyPattern._choice(p) for p in list(self._pd)]
        return pattern

class Melody(MelodyPattern):
    def __init__(
            self, 
            randomness,
            bar_length=1,
            division_count=16,
            measure=(4,4),
            pattern=None, 
            notes=[], 
            velocity=[]
        ):
        super().__init__(randomness, bar_length, division_count, measure)
        self.notes = notes
        self.velocity = velocity

        # randomness와 pattern을 동시에 넘겨주면, randomness는 pattern에 영향을 주지 않음.
        # 즉, 주어진 pattern으로 고정.
        if (pattern != None):
            self.pattern = pattern

    def set_melody(self, notes):
        pass

# testing melody pattern
if __name__ == '__main__':
    '''
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
    '''
    
    randomness = 0.5
    division_count = 16
    bar_length = 1
   
    k = 1
    for i in np.linspace(0, 1, 4):
        p = MelodyPattern(
            randomness=i,
            bar_length=bar_length,
            division_count=division_count,
            measure=(4,4)
        )

        # print(p._pd)
        
        plt.subplot(2, 2, k)
        plt.ylim([0, 1.1])
        x = np.arange(division_count * bar_length)
        plt.bar(x, p._pd)
        plt.title(f'r = {i:.2f}')

        k += 1

    plt.tight_layout()
    plt.show()
