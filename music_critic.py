import chordparser


def MusicCritic(object):
    def __init__(self):
        self._cp = chordparser.Parser()

    def get_simplicity_score(self, chords_sequence: list)
        return 0

    def count_chords_in_scale(self, chords_sequence, scale: chordparser.music.scales.Scale):
        return len([c for c in chords_sequence if g


