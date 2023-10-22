import chordparser
from chord_tokenizer import NOTE_TO_TOKEN
# from pychord import Chord
# from pychord.constants import VAL_NOTE_DICT, NOTE_VAL_DICT
# from pychord.constants.scales import RELATIVE_KEY_DICT


class ChordsMatchCriteria(object):
    def __init__(self, scale, chords, cp):
        self.scale = scale
        self.chords = chords
        self.cp = cp
        self.score = self.calc_score()

    def calc_score(self):
        raise NotImplementedError

class DiatomicMatchCriteria(ChordsMatchCriteria):
    def calc_score(self):
        diatonic_roles = [self.cp.analyse_diatonic(c, self.scale) for c in self.chords]
        matches_count = len([r for r in diatonic_roles if r])
        score = matches_count / len(self.chords)
        return score
    
class BorrowedChordsMatchCriteria(ChordsMatchCriteria):
    def calc_score(self):
        diatonic_roles = [self.cp.analyse_all(c, self.scale) for c in self.chords]
        matched_modes = [r for r in diatonic_roles
                         if (r[1], self.scale.key.mode) in [('major', 'minor'), ('minor', 'major')]]
        matches_count = len(matched_modes)
        score = matches_count / len(self.chords)
        return score

class FirstChordMatchCriteria(ChordsMatchCriteria):
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[0], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == 'I':
                return 1
            if function == 'V':
                return 0.5
        return 0
    
class LastChordMatchCriteria(ChordsMatchCriteria):
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[-1], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == 'I':
                return 1
        return 0

def find_all_sublist(target: list, pattern: list):
    if len(pattern) > len(target):
        return []
    
    all_occurences = [i for i in range(len(target) - len(pattern) + 1)
                        if pattern == target[i : i + len(pattern)]]
    return all_occurences

class ChordsProgressionsCoverageCriteria(ChordsMatchCriteria):
    """
    Appendix of "7" is not mandatory for match but increases the score
    """
    # NOTE: Major is in uppercase, minor is in lowercase.
    MAJOR_CHORDS_PROGRESSIONS = [
        ['I', 'V', 'vi', 'IV'], # 1564
        ['I', 'IV', 'I', 'V', 'vi', 'I'], # twelve bar blues variation
        ['I', 'IV', 'I', 'V', 'vi', 'I', 'V'], # twelve bar blues variation
        ['I', 'IV', 'I', 'V', 'I'], # twelve bar blues variation
        ['I', 'IV', 'I', 'IV', 'I', 'V', 'I'], # twelve bar blues variation
        ['I', 'IV', 'I', 'I7', 'IV', 'IV7', 'I', 'I7', 'V', 'IV', 'I', 'I7'], # twelve bar variation: Seventh chords
        ['I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I'], # twelve bar blues variation
        ['I', 'IV', 'I', 'IV', 'I', 'V', 'VI', 'I', 'V'], # twelve bar blues variation
        ['IV', 'I', 'V', 'VI', 'I'], # twelve bar blues variation
        ['I', 'IV', 'I', 'V', 'I', 'vi', 'I' ,'V'], # twelve bar blues variation
    ]
    
    NATURAL_MINOR_CHORDS_PROGRESSIONS = [
        ['i', 'VI', 'III', 'VII'], # 1564
    ]

    HARMONIC_MINOR_CHORDS_PROGRESSIONS = [
        ['i7', 'iv7', 'i7', 'VI7', 'v7', 'i7'], # twelve bar blues variation
    ]

    @classmethod
    def get_chords_progressions(cls, scale):
        if scale.key.mode == 'major':
            return cls.MAJOR_CHORDS_PROGRESSIONS
        if scale.key.mode == 'minor':
            if scale.key.submode == 'natural':
                return cls.NATURAL_MINOR_CHORDS_PROGRESSIONS
            if scale.key.submode == 'harmonic':
                return cls.HARMONIC_MINOR_CHORDS_PROGRESSIONS

        # return []
        raise TypeError('Unknown scale')
    
    @classmethod
    def chords_to_functions(cls, cp, chords, scale):
        chords_functions = []
        for chord in chords:
            f = cp.analyse_diatonic(chord, scale)
            if not f:
                chords_functions.append('')
            else:
                chords_functions.append(f[0][0].root)
        
        return chords_functions

    def calc_score(self):
        chords_progressions = self.get_chords_progressions(self.scale)
        functions = self.chords_to_functions(self.cp, self.chords, self.scale)

        best_used_map = self._calc_score_subset(functions, chords_progressions, [False] * len(functions))
        score = sum(best_used_map) / len(functions)
        return score
    
    def _calc_score_subset(self, functions, progressions, functions_used_maps):
        best_used_map = functions_used_maps
        if len(functions) <= 1:
            return functions_used_maps
        
        for prog in progressions:
            for occurence_i in find_all_sublist(functions, prog):
                end_i = occurence_i + len(prog)
                best_first_map = self._calc_score_subset(functions[:occurence_i + 1], progressions, functions_used_maps[:occurence_i] + [True])
                best_last_map = self._calc_score_subset(functions[end_i - 1 :], progressions, [True] + functions_used_maps[end_i :])
                occurrence_used_map = best_first_map + ([True] * (len(prog) - 2)) + best_last_map
                if sum(occurrence_used_map) > sum(best_used_map):
                    best_used_map = occurrence_used_map
        return best_used_map
                                

class RepetitionCriteria(ChordsMatchCriteria):
    MIN_REPETITION = 4
    def _find_repetition_mask(self):
        tested_pairs = []
        occupied_mask = [False] * len(self.chords)
        l = self.MIN_REPETITION
        for i in range(len(self.chords) - l * 2 + 1):
            reps_indexes = [i for i in find_all_sublist(self.chords, self.chords[i : i + l])
                            if (l, i, ) not in tested_pairs]
            if len(reps_indexes) <= 1:
                continue

            for i in reps_indexes:
                occupied_mask = occupied_mask[: i] + [True] * l + occupied_mask[i + l :]
            # new_submask = self._find_repetition_mask(chords, cloned_mask, tested_pairs + [(l, i, ) for i in reps_indexes])
            # if sum(new_submask) > sum(best_repetition_mask):
                # best_repetition_mask = new_submask
        
        return occupied_mask
    
    def calc_score(self):
        best_mask = self._find_repetition_mask()
        score = sum(best_mask) / len(self.chords)
        return score
    
class ScaleMatchCriteria(ChordsMatchCriteria):
    CRITERIAS_CLASSES = [DiatomicMatchCriteria, FirstChordMatchCriteria, LastChordMatchCriteria, ChordsProgressionsCoverageCriteria]
    def calc_score(self):
        critereas_scores = [criteria_cls(self.scale, self.chords, self.cp).score
                            for criteria_cls in self.CRITERIAS_CLASSES]
        return sum(critereas_scores)
    
# class ScaleMatch(object):
#     def __init__(self, scale, chords, cp, criterias=None):
#         if not criterias:
#             criterias = list()
#         self.criterias = [
#             RepetitionCriteria(scale, chords, cp)
#         ]
#         self.scale = scale
#         self.chords = chords
#         self.cp = cp
#         self.score = sum([criteria.score for criteria in self.criterias])

#     def __lt__(self, other):
#         if self.score != other.score:
#             return self.score < other.score
        
#         if self.chords[0].root != self.scale.root:
#             if self.chords[0].root == self.chords[0].root:
#                 return False
#             elif self.scale.root == self.chords[0].root:
#                 return True
   
#         # Equal
#         return False
    
#     def __le__(self, other):
#         if self.score != other.score:
#             return self.score <= other.score
        
#         if self.chords[0].root != self.scale.root:
#             if self.chords[0].root == self.chords[0].root:
#                 return False
#             elif self.scale.root == self.chords[0].root:
#                 return True
   
#         # Equal
#         return True
        
#     def __gt__(self, other):
#         if self.score != other.score:
#             return self.score > other.score
        
#         if self.chords[0].root != self.scale.key.root:
#             if self.chords[0].root == self.chords[0].root:
#                 return True
#             elif self.scale.key.root == self.chords[0].root:
#                 return False
   
#         # Equal
#         return False
        
#     def __ge__(self, other):
#         if self.score != other.score:
#             return self.score > other.score
        
#         if self.chords[0].root != self.scale.root:
#             if self.chords[0].root == self.chords[0].root:
#                 return True
#             elif self.scale.root == self.chords[0].root:
#                 return False
   
#         # Equal
#         return True
    
#     def __cmp__(self, other):
#         return self.scale == other._scale and self.chords == other._chords
    
#     def __str__(self):
#         return f'[ScaleMatch: {self.scale} score={self.score}]'
    
#     def __repr__(self):
#         return self.__str__()

class SongsChords(object):
    CRITERIA_CLASSES = [
        RepetitionCriteria
    ]
    def __init__(self, chords: list):
        self.cp = chordparser.Parser()
        self._dedup_raw_chords = self._remove_dupliate_chords(chords)
        self.chords = [self.cp.create_chord(c) for c in self._dedup_raw_chords]

    @classmethod
    def _remove_dupliate_chords(cls, chords):
        new_chords = [chords[0]]
        for chord in chords:
            if chord != new_chords[-1]:
                new_chords.append(chord)
        return new_chords

    def _find_best_scale(self):
        # The scale will be major/minor depending on the type of the first note
        best_score = 0
        best_scale = None
        scale_type = self.chords[0].quality.value # 'major' or 'minor'
        all_scales = [ScaleMatchCriteria(self.cp.create_scale(root, scale_type), self.chords, self.cp)
                      for root in NOTE_TO_TOKEN.keys()]
        best_scale_criteria = max(all_scales, key=lambda k:k.score)

        return best_scale_criteria.scale, best_scale_criteria.score
    
    def find_best_scale(self):
        best_scale, score = self._find_best_scale()
        other_criterias_score = sum([criteria_cls(best_scale, self.chords, self.cp).score for criteria_cls in self.CRITERIA_CLASSES])
        return best_scale, score + other_criterias_score

def test():
    # song = SongsChords('G B C Cm')
    song = SongsChords('C C G F C G Am Am F C C G F C G Am Am F C C G F C C G Am Am F Dm Em Bdim C C'.split())
    best_scale, score = song.find_best_scale()
    print(f'best scale is {best_scale} with score {score}')

if __name__ == '__main__':
    exit(test())