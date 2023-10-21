"""
@brief Tokenize a chord
"""

NOTE_TO_TOKEN = {
    'A': 0,
    'Bb': 1,
    'B': 2,
    'C': 3,
    'Db': 4,
    'D': 5,
    'Eb': 6,
    'E': 7,
    'F': 8,
    'Gb': 9,
    'G': 10,
    'Ab': 11
}
TOKEN_TO_NOTE = {v: k for k,v in NOTE_TO_TOKEN.items()}

_CHORD_TYPE_TO_TOKEN_RAW = {
    ('', ): 0,
    ('9', ): 1,
    ('11#', ): 2,
    ('13', ): 3,
    ('911#', ): 4,
    ('913', ): 5,
    ('11#13', ): 6,
    ('911#13', ): 7,
    ('MAJ79', 'M9', 'M79', 'maj79', 'Maj79', ): 8,
    ('MAJ711#', 'M11#', 'M711#', 'maj711#', 'Maj711#', ): 9,
    ('MAJ713', 'M13', 'M713', 'maj713', 'Maj713', ): 10,
    ('MAJ7911#', 'M911#', 'M7911#', 'maj7911#', 'Maj7911#', ): 11,
    ('MAJ7913', 'M913', 'M7913', 'maj7913', 'Maj7913', ): 12,
    ('MAJ711#13', 'M11#13', 'M711#13', 'maj711#13', 'Maj711#13', ): 13,
    ('MAJ7911#13', 'M911#13', 'M7911#13', 'maj7911#13', 'Maj7911#13', ): 14,
    ('m', ): 15,
    ('m9', ): 16,
    ('m11', ): 17,
    ('m13', ): 18,
    ('m911', ): 19,
    ('m913', ): 20,
    ('m1113', ): 21,
    ('m91113', ): 22,
    ('m79', ): 23,
    ('m711', ): 24,
    ('m713', ): 25,
    ('m7911', ): 26,
    ('m7913', ): 27,
    ('m71113', ): 28,
    ('m791113', ): 29,
    ('7', ): 30,
    ('79b', ): 31,
    ('79', ): 32,
    ('79#', ): 33,
    ('711#', ): 34,
    ('713b', ): 35,
    ('79b11#', ): 36,
    ('7911#', ): 37,
    ('79#11#', ): 38,
    ('79b13b', ): 39,
    ('7913b', ): 40,
    ('79#13b', ): 41,
    ('711#13b', ): 42,
    ('79b11#13b', ): 43,
    ('7911#13b', ): 44,
    ('79#11#13b', ): 45,
    ('6', ): 46,
    ('69', ): 47,
    ('611#', ): 48,
    ('6911#', ): 49,
    ('m6', ): 50,
    ('m69', ): 51,
    ('m611', ): 52,
    ('m6911', ): 53,
    ('Maj7', 'MAJ7', 'M', 'M7', 'maj7', ): 54,
    ('m7', ): 55,
    ('Aug', 'aug', '+', ): 56,
    ('dim', 'd', 'o', ): 57,
    ('dim9', 'd9', 'o9', ): 58,
    ('dim9#', 'd9#', 'o9#', ): 59,
    ('dim11', 'd11', 'o11', ): 60,
    ('dim13', 'd13', 'o13', ): 61,
    ('dim913', 'd913', 'o913', ): 62,
    ('dim9#11', 'd9#11', 'o9#11', ): 63,
    ('dim9#13', 'd9#13', 'o9#13', ): 64,
    ('dim1113', 'd1113', 'o1113', ): 65,
    ('dim91113', 'd91113', 'o91113', ): 66,
    ('dim9#1113', 'd9#1113', 'o9#1113', ): 67,
    ('Aug9', 'aug9', '+9', ): 68,
    ('Aug11', 'aug11', '+11', ): 69,
    ('Aug11#', 'aug11#', '+11#', ): 70,
    ('Aug911', 'aug911', '+911', ): 71,
    ('Aug911#', 'aug911#', '+911#', ): 72,
    ('Aug7', 'aug7', '+7', ): 73,
    ('Aug79', 'aug79', '+79', ): 74,
    ('Aug79b', 'aug79b', '+79b', ): 75,
    ('Aug79#', 'aug79#', '+79#', ): 76,
    ('Aug711', 'aug711', '+711', ): 77,
    ('Aug711#', 'aug711#', '+711#', ): 78,
    ('Aug713', 'aug713', '+713', ): 79,
    ('Aug79b11', 'aug79b11', '+79b11', ): 80,
    ('Aug79b11#', 'aug79b11#', '+79b11#', ): 81,
    ('Aug79b13', 'aug79b13', '+79b13', ): 82,
    ('Aug7911', 'aug7911', '+7911', ): 83,
    ('Aug7911#', 'aug7911#', '+7911#', ): 84,
    ('Aug7913', 'aug7913', '+7913', ): 85,
    ('Aug79#11', 'aug79#11', '+79#11', ): 86,
    ('Aug79#11#', 'aug79#11#', '+79#11#', ): 87,
    ('Aug79#13', 'aug79#13', '+79#13', ): 88,
    ('Aug79b1113', 'aug79b1113', '+79b1113', ): 89,
    ('Aug79b11#13', 'aug79b11#13', '+79b11#13', ): 90,
    ('Aug791113', 'aug791113', '+791113', ): 91,
    ('Aug7911#13', 'aug7911#13', '+7911#13', ): 92,
    ('Aug79#1113', 'aug79#1113', '+79#1113', ): 93,
    ('Aug79#11#13', 'aug79#11#13', '+79#11#13', ): 94,
    ('AugMAJ79b', 'AugM9b', 'AugM79b', 'Augmaj79b', 'AugMaj79b', 'augMAJ79b', 'augM9b', 'augM79b', 'augmaj79b', 'augMaj79b', '+MAJ79b', '+M9b', '+M79b', '+maj79b', '+Maj79b', ): 95,
    ('AugMAJ79', 'AugM9', 'AugM79', 'Augmaj79', 'AugMaj79', 'augMAJ79', 'augM9', 'augM79', 'augmaj79', 'augMaj79', '+MAJ79', '+M9', '+M79', '+maj79', '+Maj79', ): 96,
    ('AugMAJ79#', 'AugM9#', 'AugM79#', 'Augmaj79#', 'AugMaj79#', 'augMAJ79#', 'augM9#', 'augM79#', 'augmaj79#', 'augMaj79#', '+MAJ79#', '+M9#', '+M79#', '+maj79#', '+Maj79#', ): 97,
    ('AugMAJ711', 'AugM11', 'AugM711', 'Augmaj711', 'AugMaj711', 'augMAJ711', 'augM11', 'augM711', 'augmaj711', 'augMaj711', '+MAJ711', '+M11', '+M711', '+maj711', '+Maj711', ): 98,
    ('AugMAJ711#', 'AugM11#', 'AugM711#', 'Augmaj711#', 'AugMaj711#', 'augMAJ711#', 'augM11#', 'augM711#', 'augmaj711#', 'augMaj711#', '+MAJ711#', '+M11#', '+M711#', '+maj711#', '+Maj711#', ): 99,
    ('AugMAJ713', 'AugM13', 'AugM713', 'Augmaj713', 'AugMaj713', 'augMAJ713', 'augM13', 'augM713', 'augmaj713', 'augMaj713', '+MAJ713', '+M13', '+M713', '+maj713', '+Maj713', ): 100,
    ('AugMAJ79b11', 'AugM9b11', 'AugM79b11', 'Augmaj79b11', 'AugMaj79b11', 'augMAJ79b11', 'augM9b11', 'augM79b11', 'augmaj79b11', 'augMaj79b11', '+MAJ79b11', '+M9b11', '+M79b11', '+maj79b11', '+Maj79b11', ): 101,
    ('AugMAJ79b11#', 'AugM9b11#', 'AugM79b11#', 'Augmaj79b11#', 'AugMaj79b11#', 'augMAJ79b11#', 'augM9b11#', 'augM79b11#', 'augmaj79b11#', 'augMaj79b11#', '+MAJ79b11#', '+M9b11#', '+M79b11#', '+maj79b11#', '+Maj79b11#', ): 102,
    ('AugMAJ79b13', 'AugM9b13', 'AugM79b13', 'Augmaj79b13', 'AugMaj79b13', 'augMAJ79b13', 'augM9b13', 'augM79b13', 'augmaj79b13', 'augMaj79b13', '+MAJ79b13', '+M9b13', '+M79b13', '+maj79b13', '+Maj79b13', ): 103,
    ('AugMAJ7911', 'AugM911', 'AugM7911', 'Augmaj7911', 'AugMaj7911', 'augMAJ7911', 'augM911', 'augM7911', 'augmaj7911', 'augMaj7911', '+MAJ7911', '+M911', '+M7911', '+maj7911', '+Maj7911', ): 104,
    ('AugMAJ7911#', 'AugM911#', 'AugM7911#', 'Augmaj7911#', 'AugMaj7911#', 'augMAJ7911#', 'augM911#', 'augM7911#', 'augmaj7911#', 'augMaj7911#', '+MAJ7911#', '+M911#', '+M7911#', '+maj7911#', '+Maj7911#', ): 105,
    ('AugMAJ7913', 'AugM913', 'AugM7913', 'Augmaj7913', 'AugMaj7913', 'augMAJ7913', 'augM913', 'augM7913', 'augmaj7913', 'augMaj7913', '+MAJ7913', '+M913', '+M7913', '+maj7913', '+Maj7913', ): 106,
    ('AugMAJ79#11', 'AugM9#11', 'AugM79#11', 'Augmaj79#11', 'AugMaj79#11', 'augMAJ79#11', 'augM9#11', 'augM79#11', 'augmaj79#11', 'augMaj79#11', '+MAJ79#11', '+M9#11', '+M79#11', '+maj79#11', '+Maj79#11', ): 107,
    ('AugMAJ79#11#', 'AugM9#11#', 'AugM79#11#', 'Augmaj79#11#', 'AugMaj79#11#', 'augMAJ79#11#', 'augM9#11#', 'augM79#11#', 'augmaj79#11#', 'augMaj79#11#', '+MAJ79#11#', '+M9#11#', '+M79#11#', '+maj79#11#', '+Maj79#11#', ): 108,
    ('AugMAJ79#13', 'AugM9#13', 'AugM79#13', 'Augmaj79#13', 'AugMaj79#13', 'augMAJ79#13', 'augM9#13', 'augM79#13', 'augmaj79#13', 'augMaj79#13', '+MAJ79#13', '+M9#13', '+M79#13', '+maj79#13', '+Maj79#13', ): 109,
    ('AugMAJ79b1113', 'AugM9b1113', 'AugM79b1113', 'Augmaj79b1113', 'AugMaj79b1113', 'augMAJ79b1113', 'augM9b1113', 'augM79b1113', 'augmaj79b1113', 'augMaj79b1113', '+MAJ79b1113', '+M9b1113', '+M79b1113', '+maj79b1113', '+Maj79b1113', ): 110,
    ('AugMAJ79b11#13', 'AugM9b11#13', 'AugM79b11#13', 'Augmaj79b11#13', 'AugMaj79b11#13', 'augMAJ79b11#13', 'augM9b11#13', 'augM79b11#13', 'augmaj79b11#13', 'augMaj79b11#13', '+MAJ79b11#13', '+M9b11#13', '+M79b11#13', '+maj79b11#13', '+Maj79b11#13', ): 111,
    ('AugMAJ791113', 'AugM91113', 'AugM791113', 'Augmaj791113', 'AugMaj791113', 'augMAJ791113', 'augM91113', 'augM791113', 'augmaj791113', 'augMaj791113', '+MAJ791113', '+M91113', '+M791113', '+maj791113', '+Maj791113', ): 112,
    ('AugMAJ7911#13', 'AugM911#13', 'AugM7911#13', 'Augmaj7911#13', 'AugMaj7911#13', 'augMAJ7911#13', 'augM911#13', 'augM7911#13', 'augmaj7911#13', 'augMaj7911#13', '+MAJ7911#13', '+M911#13', '+M7911#13', '+maj7911#13', '+Maj7911#13', ): 113,
    ('AugMAJ79#1113', 'AugM9#1113', 'AugM79#1113', 'Augmaj79#1113', 'AugMaj79#1113', 'augMAJ79#1113', 'augM9#1113', 'augM79#1113', 'augmaj79#1113', 'augMaj79#1113', '+MAJ79#1113', '+M9#1113', '+M79#1113', '+maj79#1113', '+Maj79#1113', ): 114,
    ('AugMAJ79#11#13', 'AugM9#11#13', 'AugM79#11#13', 'Augmaj79#11#13', 'AugMaj79#11#13', 'augMAJ79#11#13', 'augM9#11#13', 'augM79#11#13', 'augmaj79#11#13', 'augMaj79#11#13', '+MAJ79#11#13', '+M9#11#13', '+M79#11#13', '+maj79#11#13', '+Maj79#11#13', ): 115,
    ('AugMAJ7', 'AugM', 'AugM7', 'Augmaj7', 'AugMaj7', 'augMAJ7', 'augM', 'augM7', 'augmaj7', 'augMaj7', '+MAJ7', '+M', '+M7', '+maj7', '+Maj7', ): 116,
    ('dim7', 'd7', 'o7', ): 117,
    ('dim79', 'd79', 'o79', ): 118,
    ('dim79#', 'd79#', 'o79#', ): 119,
    ('dim711', 'd711', 'o711', ): 120,
    ('dim7911', 'd911', 'o911', ): 121,
    ('dim79#11', 'd79#11', 'o79#11', ): 122,
    ('dim7913', 'd7913', 'o7913', ): 123,
    ('dim79#13', 'd79#13', 'o79#13', ): 124,
    ('dim71113', 'd71113', 'o71113', ): 125,
    ('dim791113', 'd791113', 'o791113', ): 126,
    ('dim79#1113', 'd9#71113', 'o79#1113', ): 127,
#TODO: take care of half-diminished symbol
    ('m7b5', ): 128,
    ('m7b59', ): 129,
    ('m7b59#', ): 130,
    ('m7b511', ): 131,
    ('m7b513b', ): 132,
    ('m7b5911', ): 133,
    ('m7b5913b', ): 134,
    ('m7b59#11', ): 135,
    ('m7b59#13b', ): 136,
    ('m7b51113b', ): 137,
    ('m7b591113b', ): 138,
    ('m7b59#1113', ): 139,
    ('sus4', '4', ): 140,
    ('sus2', '2', ): 141,
}
# Flatten the dict
CHORD_TYPE_TO_TOKEN = dict()
for all_keys, v in _CHORD_TYPE_TO_TOKEN_RAW.items():
   CHORD_TYPE_TO_TOKEN.update([(k, v, ) for k in all_keys])

TOKEN_TO_CHORD_TYPE = {v: k for k, v in _CHORD_TYPE_TO_TOKEN_RAW.items()}

SHARP_TO_FLAT = {
   'C#': 'Db',
   'D#': 'Eb',
   'F#': 'Gb',
   'G#': 'Ab',
   'A#': 'Bb',
}

class ChordTokenizer():
    @classmethod
    def tokenize(cls, chord):
        #TODO: check handling of o (diminished) and half-diminished symbols
        poss_chords_combs_num = 142
        slash_ind = -1 #by default - empty
        #root - first 2 letters in the chord
        if(len(chord) == 1):
          root = chord[0]
        elif chord[1]=='#' or chord[1]=='b':
          root = chord[0:2]
          # Convert sharp (#) to flat (b)
          if root in SHARP_TO_FLAT:
             root = SHARP_TO_FLAT[root]
        else:
          root = chord[0]

        #convert root from string to num
        root_ind = NOTE_TO_TOKEN[root]
        #bass - /
        if len(chord) >= 3 and '/' in chord[-3 :]:
          slash_ind = chord.find('/')
          bass = chord[slash_ind + 1 :]
          # Convert sharp (#) to flat (b)
          if bass in SHARP_TO_FLAT:
             bass = SHARP_TO_FLAT[bass]
        else:
          bass = root

        #convert bass from string to num
        bass_ind = NOTE_TO_TOKEN[bass]

        #type
        if len(chord) == 1:
          chord_type = ''
        elif slash_ind==-1:
          chord_type = chord[len(root):]
        else:
          chord_type = chord[len(root):slash_ind]
    
        if chord_type and chord_type not in CHORD_TYPE_TO_TOKEN:
           # Invalid chord type
           return 0

        type_ind = CHORD_TYPE_TO_TOKEN[chord_type]
        return sum([((12 ** i) * val) for i,val in enumerate([root_ind, bass_ind, type_ind])]) + 1

    @classmethod
    def detokenize(cls, token):
       if token == 0:
          return ''
       token -= 1
       root_ind = (token // (12 ** 0)) % 12
       bass_ind = (token // (12 ** 1)) % 12
       type_ind = (token // (12 ** 2)) % 144
       # root_ind, bass_ind, type_ind = [(token // (12 ** i)) % (12 ** (i + 1)) for i in range(3)]
       root = TOKEN_TO_NOTE[root_ind].upper()
       bass = TOKEN_TO_NOTE[bass_ind].upper()
       type = TOKEN_TO_CHORD_TYPE[type_ind][0]
       bass_appendix = '' if bass == root else f'/{bass}'
       return f'{root}{type}{bass_appendix}'

def test():
   print(f'C tokenization: {ChordTokenizer.tokenize("C")}')
   print(f'C de+tokenization: {ChordTokenizer.detokenize(ChordTokenizer.tokenize("F79/D"))}')

if __name__ == '__main__':
   test()