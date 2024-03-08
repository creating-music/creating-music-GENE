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
        # 모든 패턴들의 길이가 같아야 함.
        pattern_lengths = set(map(len, [kick_pattern, hihat_pattern, snare_pattern, cymbals_pattern]))
        if len(pattern_lengths) != 1:
            raise Exception("Length of patterns don't match!")
        
        # 각각 midi mapping
        kick_pattern = np.array(kick_pattern) * DrumPattern.KEYMAP['base_drum']
        hihat_pattern = np.array(hihat_pattern) * DrumPattern.KEYMAP['hihat_closed']
        snare_pattern = np.array(snare_pattern) * DrumPattern.KEYMAP['snare_drum']
        cymbals_pattern = np.array(cymbals_pattern) * DrumPattern.KEYMAP['cymbals_crash']

        self.pattern = list(zip(kick_pattern, hihat_pattern, snare_pattern, cymbals_pattern))
        self.division = division
        self.bar_length = bar_length


drum_patterns = [
    DrumPattern(
        kick_pattern  = [1, 0, 0, 0, 0, 1, 0, 0] * 4,
        hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1] * 4,
        snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0] * 4,
        cymbals_pattern=[1, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] * 3,

        division=8,
        bar_length=4,
    )
]
