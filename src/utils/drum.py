import numpy as np

class DrumPattern():
    KEYMAP = {
        'base_drum': 36,
        'snare_drum': 38,
        'hihat_closed': 42,
        'hihat_opened': 46,
        'cymbals_crash': 49,
    }
    def __init__(
        self, 
        kick_pattern: list[int], 
        hihat_pattern: list[int], 
        snare_pattern: list[int], 
        cymbals_pattern: list[int],
        division: int = 8,
        bar_length: int = 1,
    ):        
        # 각각 midi mapping
        kick_pattern_mapped = np.array(kick_pattern) * DrumPattern.KEYMAP['base_drum']
        snare_pattern_mapped = np.array(snare_pattern) * DrumPattern.KEYMAP['snare_drum']
        hihat_pattern_mapped = np.array(hihat_pattern) * DrumPattern.KEYMAP['hihat_closed']
        cymbals_pattern_mapped = np.array(cymbals_pattern) * DrumPattern.KEYMAP['cymbals_crash']

        drums = [
            kick_pattern_mapped, 
            snare_pattern_mapped, 
            hihat_pattern_mapped, 
            cymbals_pattern_mapped
        ]
        pattern_lengths = set(map(len, drums))

        # 모든 패턴들의 길이가 같아야 함.
        if len(pattern_lengths) != 1:
            raise Exception("Length of patterns don't match!")

        self.pattern = list(zip(*drums))
        self.division = division
        self.bar_length = bar_length


drum_patterns = [
    DrumPattern(
        kick_pattern =  [0],
        hihat_pattern = [0],
        snare_pattern = [0],
        cymbals_pattern=[0],

        division=1,
        bar_length=1,
    ),
    DrumPattern(
        kick_pattern  = [1, 0, 0, 0, 0, 1, 0, 0] * 4,
        snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0] * 4,
        hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1] * 4,
        cymbals_pattern=[1, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] * 3,

        division=8,
        bar_length=4,
    )
]
