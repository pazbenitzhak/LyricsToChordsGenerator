import chordparser
from chord_tokenizer import NOTE_TO_TOKEN
# from pychord import Chord
# from pychord.constants import VAL_NOTE_DICT, NOTE_VAL_DICT
# from pychord.constants.scales import RELATIVE_KEY_DICT


class ScaleMatchCriteria(object):
    def __init__(self, scale, chords, cp):
        self.scale = scale
        self.chords = chords
        self.cp = cp
        self.score = self.calc_score()

    def calc_score(self):
        raise NotImplementedError


class DiatomicMatchCriteria(ScaleMatchCriteria):
    def calc_score(self):
        diatonic_roles = [self.cp.analyse_diatonic(c, self.scale) for c in self.chords]
        matches_count = len([r for r in diatonic_roles if r])
        score = matches_count / len(self.chords)
        return score

class FirstChordMatchCriteria(ScaleMatchCriteria):
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[0], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == 'I':
                return 1
            if function == 'V':
                return 0.5
        return 0
    
class LastChordMatchCriteria(ScaleMatchCriteria):
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[-1], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == 'I':
                return 1
        return 0

class ChordsProgressionsCoverageCriteria(ScaleMatchCriteria):
    CHORDS_PROGRESSIONS = []
    
    def calc_score(self):
        # results = self.cp.analyse_diatonic(self.chords[-1], self.scale)
        # if results:  # diatonic
            # function = results[0][0].root  # just show roman notation
            # if function == 'I':
                # return 1
        return 0
    
    
class ChordsProgressionsCoverageCriteria(ChordsProgressionsCoverageCriteria):
    MAJOR_CHORDS_PROGRESSIONS = [
        ('I', 'V', 'VI', 'IV') # 1564
        ('I', 'IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'VI', 'I', 'V') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'I7', 'IV', 'IV7', 'I', 'I7', 'V', 'IV', 'I', 'I7') # twelve bar variation: Seventh chords
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I', 'V') # twelve bar blues variation
        ('IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'I', 'VI', 'I' ,'V') # twelve bar blues variation
    ]
    
    MINOR_CHORDS_PROGRESSIONS = [
        ('I', 'VI', 'III', 'VII') # 1564

        ('I', 'IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'VI', 'I', 'V') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'I7', 'IV', 'IV7', 'I', 'I7', 'V', 'IV', 'I', 'I7') # twelve bar variation: Seventh chords
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I', 'V') # twelve bar blues variation
        ('IV', 'I', 'V', 'VI', 'I') # twelve bar blues variation
        ('I', 'IV', 'I', 'V', 'I', 'VI', 'I' ,'V') # twelve bar blues variation

    ]
        
class RepetitionChorusCriteria(ScaleMatchCriteria):
    def calc_score(self):
        # results = self.cp.analyse_diatonic(self.chords[-1], self.scale)
        # if results:  # diatonic
            # function = results[0][0].root  # just show roman notation
            # if function == 'I':
                # return 1
        return 0
    
class ScaleMatch(object):
    def __init__(self, scale, chords, cp, criterias=None):
        if not criterias:
            criterias = list()
        self.criterias = [
            DiatomicMatchCriteria(scale, chords, cp),
            FirstChordMatchCriteria(scale, chords, cp),
            LastChordMatchCriteria(scale, chords, cp)
        ]
        self.scale = scale
        self.chords = chords
        self.cp = cp
        self.score = sum([criteria.score for criteria in self.criterias])

    def __lt__(self, other):
        if self.score != other.score:
            return self.score < other.score
        
        if self.chords[0].root != self.scale.root:
            if self.chords[0].root == self.chords[0].root:
                return False
            elif self.scale.root == self.chords[0].root:
                return True
   
        # Equal
        return False
    
    def __le__(self, other):
        if self.score != other.score:
            return self.score <= other.score
        
        if self.chords[0].root != self.scale.root:
            if self.chords[0].root == self.chords[0].root:
                return False
            elif self.scale.root == self.chords[0].root:
                return True
   
        # Equal
        return True
        
    def __gt__(self, other):
        if self.score != other.score:
            return self.score > other.score
        
        if self.chords[0].root != self.scale.key.root:
            if self.chords[0].root == self.chords[0].root:
                return True
            elif self.scale.key.root == self.chords[0].root:
                return False
   
        # Equal
        return False
        
    def __ge__(self, other):
        if self.score != other.score:
            return self.score > other.score
        
        if self.chords[0].root != self.scale.root:
            if self.chords[0].root == self.chords[0].root:
                return True
            elif self.scale.root == self.chords[0].root:
                return False
   
        # Equal
        return True
    
    def __cmp__(self, other):
        return self.scale == other._scale and self.chords == other._chords
    
    def __str__(self):
        return f'[ScaleMatch: {self.scale} score={self.score}]'
    
    def __repr__(self):
        return self.__str__()

class SongsChords(object):
    def __init__(self, chords: list):
        self.cp = chordparser.Parser()
        self._raw_chords = chords
        self._chords = [self.cp.create_chord(c) for c in chords.split()]

    def find_best_scale(self):
        # The scale will be major/minor depending on the type of the first note
        best_score = 0
        best_scale = None
        scale_type = self._chords[0].quality.value # 'major' or 'minor'
        all_scales = [ScaleMatch(self.cp.create_scale(root, scale_type), self._chords, self.cp) for root in NOTE_TO_TOKEN.keys()]
        best_scale = max(all_scales)

        return best_scale

def test():
    song = SongsChords('G B C Cm')
    best_scale = song.find_best_scale()
    print(f'best scale is {best_scale}')

if __name__ == '__main__':
    exit(test())