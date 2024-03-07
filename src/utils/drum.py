class DrumPattern():
    def __init__(
        self, 
        kick_pattern: list[int], 
        hihat_pattern: list[int], 
        snare_pattern: list[int], 
        cymbals_pattern: list[int],
        division: int = 8,
        bar_length: int = 1,
    ):
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
