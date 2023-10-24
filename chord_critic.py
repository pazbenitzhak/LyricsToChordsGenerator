import chordparser
from chord_tokenizer import NOTE_TO_TOKEN
import numpy as np
# from pychord import Chord
# from pychord.constants import VAL_NOTE_DICT, NOTE_VAL_DICT
# from pychord.constants.scales import RELATIVE_KEY_DICT


def find_all_sublist(target: list, pattern: list):
    if len(pattern) > len(target):
        return []
    
    all_occurences = [i for i in range(len(target) - len(pattern) + 1)
                        if pattern == target[i : i + len(pattern)]]
    return all_occurences


class Criteria(object):
    def __init__(self, scale, chords, cp):
        self.scale = scale
        self.chords = chords
        self.cp = cp
        self.score = self.calc_score()

    def calc_score(self):
        raise NotImplementedError
    
    def __lt__(self, other):
        return self.calc_score().__lt__(other.calc_score())

    def __le__(self, other):
        return self.calc_score().__le__(other.calc_score())

    def __gt__(self, other):
        return self.calc_score().__gt__(other.calc_score())

    def __ge__(self, other):
        return self.calc_score().__ge__(other.calc_score())
    
    def __eq__(self, other):
        return self.calc_score().__eq__(other.calc_score())

    def __ne__(self, other):
        return self.calc_score().__ne__(other.calc_score())


class InScaleCriteria(Criteria):
    """
    Percentage of chords that are degree in the diatonic scale
    """
    def calc_score(self):
        diatonic_roles = [self.cp.analyse_diatonic(c, self.scale) for c in self.chords]
        matches_count = len([r for r in diatonic_roles if r])
        score = matches_count / len(self.chords)
        return score
    
class BorrowedScaleCriteria(Criteria):
    """
    Percentage of chords that are borrowed chords in the diatonic scale
    """
    def calc_score(self):
        secondary_scale = self.cp.create_scale(self.scale.key.root, 'major' if self.scale.key.mode == 'minor' else 'minor')
        secondary_roles = [self.cp.analyse_diatonic(c, secondary_scale) for c in self.chords]
        matched_modes = [r for r in secondary_roles if r]
        matches_count = len([m for m in matched_modes if m])
        score = matches_count / len(self.chords)
        return score

class FirstScoreCriteria(Criteria):
    """
    Match between the first chord and the scale
    """
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[0], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == ('I' if self.scale.key.mode == 'major' else 'i'):
                return 1
            if function == 'V':
                second_function = self.cp.analyse_diatonic(self.chords[1], self.scale)
                if second_function == ('I' if self.scale.key.mode == 'major' else 'i'):
                    return 0.5
        return 0
    
class LastScoreCriteria(Criteria):
    def calc_score(self):
        results = self.cp.analyse_diatonic(self.chords[-1], self.scale)
        if results:  # diatonic
            function = results[0][0].root  # just show roman notation
            if function == ('I' if self.scale.key.mode == 'major' else 'i'):
                return 1
        return 0

class ChordsProgressionsCoverageCriteria(Criteria):
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
        ['I', 'IV', 'V'],
    ]
    
    NATURAL_MINOR_CHORDS_PROGRESSIONS = [
        ['i', 'VI', 'III', 'VII'], # 1564
        ['i', 'III', 'VII', 'IV'], # Boulevards of broken dreams 1
        ['VI', 'III', 'VII', 'i'] # Boulevards of broken dreams 2
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
                other_scale = cp.create_scale(scale.key.root, 'major' if scale.key.mode == 'minor' else 'minor')
                f = cp.analyse_diatonic(chord, other_scale)
                if not f:
                    chords_functions.append('')
                    continue
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
                best_used_map = best_used_map[: occurence_i] + ([True] * len(prog)) + best_used_map[occurence_i + len(prog) :]
            pass
        return best_used_map
                                

class RepetitionCoverageCriteria(Criteria):
    MIN_REPETITION = 4
    def _find_repetition_mask(self):
        tested_pairs = {}
        occupied_mask = [False] * len(self.chords)
        l = self.MIN_REPETITION
        chords_tuple = tuple([str(chord) for chord in self.chords])
        for i in range(len(self.chords) - l + 1):
            curr = chords_tuple[i : i + l]
            reps_indexes = tested_pairs.setdefault(curr, list())
            reps_indexes.append(i)
            if len(reps_indexes) > 1:
                for i in reps_indexes:
                    occupied_mask = occupied_mask[: i] + [True] * l + occupied_mask[i + l :]
        
        return occupied_mask
    
    def calc_score(self):
        best_mask = self._find_repetition_mask()
        score = sum(best_mask) / len(self.chords)
        return score
    
    
class LocalScaleCriteria(Criteria):
    """
    Scale criteria for a specific scale, not necessarily the best
    """
    def calc_score(self):
        self.first_score = FirstScoreCriteria(self.scale, self.chords, self.cp).score
        self.last_score = LastScoreCriteria(self.scale, self.chords, self.cp).score
        self.inscale_score = InScaleCriteria(self.scale, self.chords, self.cp).score
        self.borscale_score = BorrowedScaleCriteria(self.scale, self.chords, self.cp).score
        total = self.first_score + self.last_score + (1.5 * self.inscale_score) + (0.5 * self.borscale_score) + 1
        # print(f'Testing scale {str(self.scale.key)}: {total}')
        return total
    

class ScaleCriteria(Criteria):
    def __init__(self, scale, chords, cp):
        super(ScaleCriteria, self).__init__(scale, chords, cp)
        self._best_scale_criteria = None

    @property
    def best_scale_criteria(self):
        if self._best_scale_criteria is None:
            self.calc_score()
        return self._best_scale_criteria
    
    def _get_all_scales_criteria(self):
        # The scale will be major/minor depending on the type of the first note
        all_major_scales = [LocalScaleCriteria(self.cp.create_scale(root, 'major'), self.chords, self.cp)
                            for root in NOTE_TO_TOKEN.keys()]
        all_minor_scales = [LocalScaleCriteria(self.cp.create_scale(root, 'minor'), self.chords, self.cp)
                            for root in NOTE_TO_TOKEN.keys()]
        all_scales = all_major_scales + all_minor_scales

        return all_scales

    def calc_score(self):
        all_criterias = self._get_all_scales_criteria()
        best_criteria = max(all_criterias, key=lambda c:c.score)
        # Softmax
        score = np.exp(best_criteria.score) / np.sum(np.exp([c.score for c in all_criterias]))
        self._best_scale_criteria = best_criteria
        return score
        

class ArtCriteria(Criteria):
    def __init__(self, best_scale, chords, cp, best_scale_criteria):
        self.best_scale_criteria = best_scale_criteria
        super(ArtCriteria, self).__init__(best_scale, chords, cp)

    def calc_score(self):
        best_scale_criteria = self.best_scale_criteria
        in_scale = best_scale_criteria.inscale_score
        bor_scale = best_scale_criteria.borscale_score
        result = np.exp(bor_scale) / (np.exp(bor_scale) + np.exp(in_scale) + np.e)
        return result

class StructureCriteria(Criteria):
    def calc_score(self):
        chord_progression_coverage = ChordsProgressionsCoverageCriteria(self.scale, self.chords, self.cp)
        repetition_coverage = RepetitionCoverageCriteria(self.scale, self.chords, self.cp)
        cpc = chord_progression_coverage.score
        rc = repetition_coverage.score
        # print(f'cpc={cpc}, rc={rc}')
        arithmetic_avg = 0.5 * (cpc + rc)
        geometric_avg = np.sqrt(cpc * rc)
        result = 0.5 * (arithmetic_avg + geometric_avg)
        return result

class ChordsMetrics(object):
    def __init__(self, chords: list):
        self.cp = chordparser.Parser()
        self._dedup_raw_chords = self._remove_dupliate_chords(chords)
        self.chords = []
        for chord in self._dedup_raw_chords:
            try:
                self.chords.append(self.cp.create_chord(chord))
            except Exception as e:
                # print(f'Error: skipping chord {chord} - {e}')
                pass
        # self.chords = [self.cp.create_chord(c) for c in self._dedup_raw_chords]
        self._scale_criteria = ScaleCriteria(None, self.chords, self.cp)
        self._art_criteria = ArtCriteria(self.best_scale_criteria.scale, self.chords, self.cp, self.best_scale_criteria)
        self._structure_criteria = StructureCriteria(self.best_scale_criteria.scale, self.chords, self.cp)

    @classmethod
    def _remove_dupliate_chords(cls, chords):
        new_chords = [chords[0]]
        for chord in chords:
            if chord != new_chords[-1]:
                new_chords.append(chord)
        return new_chords
    
    @property
    def best_scale_criteria(self):
        return self._scale_criteria.best_scale_criteria

    @property
    def scale_score(self):
        return self._scale_criteria.score
        
    @property
    def art_score(self):
        return self._art_criteria.score
    
    @property
    def structure_score(self):
        return self._structure_criteria.score
    
    @property
    def scores(self):
        return self.scale_score, self.art_score, self.structure_score

    
def test():
    # metrics = ChordsMetrics('Em G D A Em G D A C G D Em C G D Em'.split())
    metrics = ChordsMetrics('C G Am F C G Am F'.split())
    best_scale = metrics.best_scale_criteria.scale
    scores = metrics.scores
    print(f'best scale is {best_scale} with scores {scores}')

if __name__ == '__main__':
    exit(test())