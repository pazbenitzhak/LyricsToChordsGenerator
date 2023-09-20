class MyTokenizer():
    def tokenize(self, chord):
        #TODO: check handling of o (diminished) and half-diminished symbols
        poss_chords_combs_num = 142
        slash_ind = -1 #by default - empty
        #root - first 2 letters in the chord
        if(len(chord) == 1):
          root = chord[0].lower()
        elif chord[1]=='#' or chord[1]=='b':
          root = chord[0:2].lower()
          #handle case of 'duplicate notes'
          if root=="db":
            root = "c#"
          elif root=="d#":
            root = "eb"
          elif root=="gb":
            root = "f#"
          elif root=="g#":
            root = "ab"
          elif root=="a#":
            root = "bb"
        else:
          root = chord[0].lower()

        #convert root from string to num
        if root=='a':
          root_ind = 0
        elif root=='bb':
          root_ind = 1
        elif root=='b':
          root_ind = 2
        elif root=='c':
          root_ind = 3
        elif root=='c#':
          root_ind = 4
        elif root=='d':
          root_ind = 5
        elif root=='eb':
          root_ind = 6
        elif root=='e':
          root_ind = 7
        elif root=='f':
          root_ind = 8
        elif root=='f#':
          root_ind = 9
        elif root=='g':
          root_ind = 10
        elif root=='ab':
          root_ind = 11
        else:
          return 0
        #bass - /
        if len(chord) >= 3 and '/' in chord[-3:]:
          slash_ind = chord.find('/')
          bass = chord[slash_ind+1:].lower()
          if bass=="db":
            bass = "c#"
          elif bass=="d#":
            bass = "eb"
          elif bass=="gb":
            bass = "f#"
          elif bass=="g#":
            bass = "ab"
          elif bass=="a#":
            bass = "bb"
        else:
          bass = root


        #convert bass from string to num
        if bass=='a':
          bass_ind = 0
        elif bass=='bb':
          bass_ind = 1
        elif bass=='b':
          bass_ind = 2
        elif bass=='c':
          bass_ind = 3
        elif bass=='c#':
          bass_ind = 4
        elif bass=='d':
          bass_ind = 5
        elif bass=='eb':
          bass_ind = 6
        elif bass=='e':
          bass_ind = 7
        elif bass=='f':
          bass_ind = 8
        elif bass=='f#':
          bass_ind = 9
        elif bass=='g':
          bass_ind = 10
        elif bass=='ab':
          bass_ind = 11
        else:
          return 0


        #type
        if len(chord) == 1:
          chord_type = ''
        elif slash_ind==-1:
          chord_type = chord[len(root):]
        else:
          chord_type = chord[len(root):slash_ind]
        if chord_type == '':
            type_ind = 0
        elif chord_type == '9':
            type_ind = 1
        elif chord_type == '11#':
            type_ind = 2
        elif chord_type == '13':
            type_ind = 3
        elif chord_type == '911#':
            type_ind = 4
        elif chord_type == '913':
            type_ind = 5
        elif chord_type == '11#13':
            type_ind = 6
        elif chord_type == '911#13':
            type_ind = 7
        elif chord_type == 'MAJ79' or chord_type == 'M9' or \
        chord_type == 'M79' or chord_type == 'maj79' or chord_type == 'Maj79':
            type_ind = 8
        elif chord_type == 'MAJ711#' or chord_type == 'M11#' or \
        chord_type == 'M711#' or chord_type == 'maj711#' or chord_type == 'Maj711#':
            type_ind = 9
        elif chord_type == 'MAJ713' or chord_type == 'M13' or \
        chord_type == 'M713' or chord_type == 'maj713' or chord_type == 'Maj713':
            type_ind = 10
        elif chord_type == 'MAJ7911#' or chord_type == 'M911#' or \
        chord_type == 'M7911#' or chord_type == 'maj7911#' or chord_type == 'Maj7911#':
            type_ind = 11
        elif chord_type == 'MAJ7913' or chord_type == 'M913' or \
        chord_type == 'M7913' or chord_type == 'maj7913' or chord_type == 'Maj7913':
            type_ind = 12
        elif chord_type == 'MAJ711#13' or chord_type == 'M11#13' or \
        chord_type == 'M711#13' or chord_type == 'maj711#13' or chord_type == 'Maj711#13':
            type_ind = 13
        elif chord_type == 'MAJ7911#13' or chord_type == 'M911#13' or \
        chord_type == 'M7911#13' or chord_type == 'maj7911#13' or chord_type == 'Maj7911#13':
            type_ind = 14
        elif chord_type == 'm':
            type_ind = 15
        elif chord_type == 'm9':
            type_ind = 16
        elif chord_type == 'm11':
            type_ind = 17
        elif chord_type == 'm13':
            type_ind = 18
        elif chord_type == 'm911':
            type_ind = 19
        elif chord_type == 'm913':
            type_ind = 20
        elif chord_type == 'm1113':
            type_ind = 21
        elif chord_type == 'm91113':
            type_ind = 22
        elif chord_type == 'm79':
            type_ind = 23
        elif chord_type == 'm711':
            type_ind = 24
        elif chord_type == 'm713':
            type_ind = 25
        elif chord_type == 'm7911':
            type_ind = 26
        elif chord_type == 'm7913':
            type_ind = 27
        elif chord_type == 'm71113':
            type_ind = 28
        elif chord_type == 'm791113':
            type_ind = 29
        elif chord_type == '7':
            type_ind = 30
        elif chord_type == '79b':
            type_ind = 31
        elif chord_type == '79':
            type_ind = 32
        elif chord_type == '79#':
            type_ind = 33
        elif chord_type == '711#':
            type_ind = 34
        elif chord_type == '713b':
            type_ind = 35
        elif chord_type == '79b11#':
            type_ind = 36
        elif chord_type == '7911#':
            type_ind = 37
        elif chord_type == '79#11#':
            type_ind = 38
        elif chord_type == '79b13b':
            type_ind = 39
        elif chord_type == '7913b':
            type_ind = 40
        elif chord_type == '79#13b':
            type_ind = 41
        elif chord_type == '711#13b':
            type_ind = 42
        elif chord_type == '79b11#13b':
            type_ind = 43
        elif chord_type == '7911#13b':
            type_ind = 44
        elif chord_type == '79#11#13b':
            type_ind = 45
        elif chord_type == '6':
            type_ind = 46
        elif chord_type == '69':
            type_ind = 47
        elif chord_type == '611#':
            type_ind = 48
        elif chord_type == '6911#':
            type_ind = 49
        elif chord_type == 'm6':
            type_ind = 50
        elif chord_type == 'm69':
            type_ind = 51
        elif chord_type == 'm611':
            type_ind = 52
        elif chord_type == 'm6911':
            type_ind = 53
        elif chord_type == 'MAJ7' or chord_type == 'M' or \
        chord_type == 'M7' or chord_type == 'maj7' or chord_type == 'Maj7':
            type_ind = 54
        elif chord_type == 'm7':
            type_ind = 55
        elif chord_type == 'Aug' or chord_type == 'aug' or \
        chord_type == '+':
            type_ind = 56
        elif chord_type == 'dim' or chord_type == 'd' or \
        chord_type == 'o':
            type_ind = 57
        elif chord_type == 'dim9' or chord_type == 'd9' or \
        chord_type == 'o9':
            type_ind = 58
        elif chord_type == 'dim9#' or chord_type == 'd9#' or \
        chord_type == 'o9#':
            type_ind = 59
        elif chord_type == 'dim11' or chord_type == 'd11' or \
        chord_type == 'o11':
            type_ind = 60
        elif chord_type == 'dim13' or chord_type == 'd13' or \
        chord_type == 'o13':
            type_ind = 61
        elif chord_type == 'dim913' or chord_type == 'd913' or \
        chord_type == 'o913':
            type_ind = 62
        elif chord_type == 'dim9#11' or chord_type == 'd9#11' or \
        chord_type == 'o9#11':
            type_ind = 63
        elif chord_type == 'dim9#13' or chord_type == 'd9#13' or \
        chord_type == 'o9#13':
            type_ind = 64
        elif chord_type == 'dim1113' or chord_type == 'd1113' or \
        chord_type == 'o1113':
            type_ind = 65
        elif chord_type == 'dim91113' or chord_type == 'd91113' or \
        chord_type == 'o91113':
            type_ind = 66
        elif chord_type == 'dim9#1113' or chord_type == 'd9#1113' or \
        chord_type == 'o9#1113':
            type_ind = 67
        elif chord_type == 'Aug9' or chord_type == 'aug9' or \
        chord_type == '+9':
            type_ind = 68
        elif chord_type == 'Aug11' or chord_type == 'aug11' or \
        chord_type == '+11':
            type_ind = 69
        elif chord_type == 'Aug11#' or chord_type == 'aug11#' or \
        chord_type == '+11#':
            type_ind = 70
        elif chord_type == 'Aug911' or chord_type == 'aug911' or \
        chord_type == '+911':
            type_ind = 71
        elif chord_type == 'Aug911#' or chord_type == 'aug911#' or \
        chord_type == '+911#':
            type_ind = 72
        elif chord_type == 'Aug7' or chord_type == 'aug7' or \
        chord_type == '+7':
            type_ind = 73
        elif chord_type == 'Aug79' or chord_type == 'aug79' or \
        chord_type == '+79':
            type_ind = 74
        elif chord_type == 'Aug79b' or chord_type == 'aug79b' or \
        chord_type == '+79b':
            type_ind = 75
        elif chord_type == 'Aug79#' or chord_type == 'aug79#' or \
        chord_type == '+79#':
            type_ind = 76
        elif chord_type == 'Aug711' or chord_type == 'aug711' or \
        chord_type == '+711':
            type_ind = 77
        elif chord_type == 'Aug711#' or chord_type == 'aug711#' or \
        chord_type == '+711#':
            type_ind = 78
        elif chord_type == 'Aug713' or chord_type == 'aug713' or \
        chord_type == '+713':
            type_ind = 79
        elif chord_type == 'Aug79b11' or chord_type == 'aug79b11' or \
        chord_type == '+79b11':
            type_ind = 80
        elif chord_type == 'Aug79b11#' or chord_type == 'aug79b11#' or \
        chord_type == '+79b11#':
            type_ind = 81
        elif chord_type == 'Aug79b13' or chord_type == 'aug79b13' or \
        chord_type == '+79b13':
            type_ind = 82
        elif chord_type == 'Aug7911' or chord_type == 'aug7911' or \
        chord_type == '+7911':
            type_ind = 83
        elif chord_type == 'Aug7911#' or chord_type == 'aug7911#' or \
        chord_type == '+7911#':
            type_ind = 84
        elif chord_type == 'Aug7913' or chord_type == 'aug7913' or \
        chord_type == '+7913':
            type_ind = 85
        elif chord_type == 'Aug79#11' or chord_type == 'aug79#11' or \
        chord_type == '+79#11':
            type_ind = 86
        elif chord_type == 'Aug79#11#' or chord_type == 'aug79#11#' or \
        chord_type == '+79#11#':
            type_ind = 87
        elif chord_type == 'Aug79#13' or chord_type == 'aug79#13' or \
        chord_type == '+79#13':
            type_ind = 88
        elif chord_type == 'Aug79b1113' or chord_type == 'aug79b1113' or \
        chord_type == '+79b1113':
            type_ind = 89
        elif chord_type == 'Aug79b11#13' or chord_type == 'aug79b11#13' or \
        chord_type == '+79b11#13':
            type_ind = 90
        elif chord_type == 'Aug791113' or chord_type == 'aug791113' or \
        chord_type == '+791113':
            type_ind = 91
        elif chord_type == 'Aug7911#13' or chord_type == 'aug7911#13' or \
        chord_type == '+7911#13':
            type_ind = 92
        elif chord_type == 'Aug79#1113' or chord_type == 'aug79#1113' or \
        chord_type == '+79#1113':
            type_ind = 93
        elif chord_type == 'Aug79#11#13' or chord_type == 'aug79#11#13' or \
        chord_type == '+79#11#13':
            type_ind = 94
        elif chord_type == 'AugMAJ79b' or chord_type == 'AugM9b' or chord_type == 'AugM79b' \
        or chord_type == 'Augmaj79b' or chord_type == 'AugMaj79b' or chord_type == 'augMAJ79b' \
        or chord_type == 'augM9b' or chord_type == 'augM79b' or chord_type == 'augmaj79b' \
        or chord_type == 'augMaj79b' or chord_type == '+MAJ79b' or chord_type == '+M9b' \
        or chord_type == '+M79b' or chord_type == '+maj79b' or chord_type == '+Maj79b':
          type_ind = 95
        elif chord_type == 'AugMAJ79' or chord_type == 'AugM9' or chord_type == 'AugM79' \
        or chord_type == 'Augmaj79' or chord_type == 'AugMaj79' or chord_type == 'augMAJ79' \
        or chord_type == 'augM9' or chord_type == 'augM79' or chord_type == 'augmaj79' \
        or chord_type == 'augMaj79' or chord_type == '+MAJ79' or chord_type == '+M9' \
        or chord_type == '+M79' or chord_type == '+maj79' or chord_type == '+Maj79':
          type_ind = 96
        elif chord_type == 'AugMAJ79#' or chord_type == 'AugM9#' or chord_type == 'AugM79#' \
        or chord_type == 'Augmaj79#' or chord_type == 'AugMaj79#' or chord_type == 'augMAJ79#' \
        or chord_type == 'augM9#' or chord_type == 'augM79#' or chord_type == 'augmaj79#' \
        or chord_type == 'augMaj79#' or chord_type == '+MAJ79#' or chord_type == '+M9#' \
        or chord_type == '+M79#' or chord_type == '+maj79#' or chord_type == '+Maj79#':
          type_ind = 97
        elif chord_type == 'AugMAJ711' or chord_type == 'AugM11' or chord_type == 'AugM711' \
        or chord_type == 'Augmaj711' or chord_type == 'AugMaj711' or chord_type == 'augMAJ711' \
        or chord_type == 'augM11' or chord_type == 'augM711' or chord_type == 'augmaj711' \
        or chord_type == 'augMaj711' or chord_type == '+MAJ711' or chord_type == '+M11' \
        or chord_type == '+M711' or chord_type == '+maj711' or chord_type == '+Maj711':
          type_ind = 98
        elif chord_type == 'AugMAJ711#' or chord_type == 'AugM11#' or chord_type == 'AugM711#' \
        or chord_type == 'Augmaj711#' or chord_type == 'AugMaj711#' or chord_type == 'augMAJ711#' \
        or chord_type == 'augM11#' or chord_type == 'augM711#' or chord_type == 'augmaj711#' \
        or chord_type == 'augMaj711#' or chord_type == '+MAJ711#' or chord_type == '+M11#' \
        or chord_type == '+M711#' or chord_type == '+maj711#' or chord_type == '+Maj711#':
          type_ind = 99
        elif chord_type == 'AugMAJ713' or chord_type == 'AugM13' or chord_type == 'AugM713' \
        or chord_type == 'Augmaj713' or chord_type == 'AugMaj713' or chord_type == 'augMAJ713' \
        or chord_type == 'augM13' or chord_type == 'augM713' or chord_type == 'augmaj713' \
        or chord_type == 'augMaj713' or chord_type == '+MAJ713' or chord_type == '+M13' \
        or chord_type == '+M713' or chord_type == '+maj713' or chord_type == '+Maj713':
          type_ind = 100
        elif chord_type == 'AugMAJ79b11' or chord_type == 'AugM9b11' or chord_type == 'AugM79b11' \
        or chord_type == 'Augmaj79b11' or chord_type == 'AugMaj79b11' or chord_type == 'augMAJ79b11' \
        or chord_type == 'augM9b11' or chord_type == 'augM79b11' or chord_type == 'augmaj79b11' \
        or chord_type == 'augMaj79b11' or chord_type == '+MAJ79b11' or chord_type == '+M9b11' \
        or chord_type == '+M79b11' or chord_type == '+maj79b11' or chord_type == '+Maj79b11':
          type_ind = 101
        elif chord_type == 'AugMAJ79b11#' or chord_type == 'AugM9b11#' or chord_type == 'AugM79b11#' \
        or chord_type == 'Augmaj79b11#' or chord_type == 'AugMaj79b11#' or chord_type == 'augMAJ79b11#' \
        or chord_type == 'augM9b11#' or chord_type == 'augM79b11#' or chord_type == 'augmaj79b11#' \
        or chord_type == 'augMaj79b11#' or chord_type == '+MAJ79b11#' or chord_type == '+M9b11#' \
        or chord_type == '+M79b11#' or chord_type == '+maj79b11#' or chord_type == '+Maj79b11#':
          type_ind = 102
        elif chord_type == 'AugMAJ79b13' or chord_type == 'AugM9b13' or chord_type == 'AugM79b13' \
        or chord_type == 'Augmaj79b13' or chord_type == 'AugMaj79b13' or chord_type == 'augMAJ79b13' \
        or chord_type == 'augM9b13' or chord_type == 'augM79b13' or chord_type == 'augmaj79b13' \
        or chord_type == 'augMaj79b13' or chord_type == '+MAJ79b13' or chord_type == '+M9b13' \
        or chord_type == '+M79b13' or chord_type == '+maj79b13' or chord_type == '+Maj79b13':
          type_ind = 103
        elif chord_type == 'AugMAJ7911' or chord_type == 'AugM911' or chord_type == 'AugM7911' \
        or chord_type == 'Augmaj7911' or chord_type == 'AugMaj7911' or chord_type == 'augMAJ7911' \
        or chord_type == 'augM911' or chord_type == 'augM7911' or chord_type == 'augmaj7911' \
        or chord_type == 'augMaj7911' or chord_type == '+MAJ7911' or chord_type == '+M911' \
        or chord_type == '+M7911' or chord_type == '+maj7911' or chord_type == '+Maj7911':
          type_ind = 104
        elif chord_type == 'AugMAJ7911#' or chord_type == 'AugM911#' or chord_type == 'AugM7911#' \
        or chord_type == 'Augmaj7911#' or chord_type == 'AugMaj7911#' or chord_type == 'augMAJ7911#' \
        or chord_type == 'augM911#' or chord_type == 'augM7911#' or chord_type == 'augmaj7911#' \
        or chord_type == 'augMaj7911#' or chord_type == '+MAJ7911#' or chord_type == '+M911#' \
        or chord_type == '+M7911#' or chord_type == '+maj7911#' or chord_type == '+Maj7911#':
          type_ind = 105
        elif chord_type == 'AugMAJ7913' or chord_type == 'AugM913' or chord_type == 'AugM7913' \
        or chord_type == 'Augmaj7913' or chord_type == 'AugMaj7913' or chord_type == 'augMAJ7913' \
        or chord_type == 'augM913' or chord_type == 'augM7913' or chord_type == 'augmaj7913' \
        or chord_type == 'augMaj7913' or chord_type == '+MAJ7913' or chord_type == '+M913' \
        or chord_type == '+M7913' or chord_type == '+maj7913' or chord_type == '+Maj7913':
          type_ind = 106
        elif chord_type == 'AugMAJ79#11' or chord_type == 'AugM9#11' or chord_type == 'AugM79#11' \
        or chord_type == 'Augmaj79#11' or chord_type == 'AugMaj79#11' or chord_type == 'augMAJ79#11' \
        or chord_type == 'augM9#11' or chord_type == 'augM79#11' or chord_type == 'augmaj79#11' \
        or chord_type == 'augMaj79#11' or chord_type == '+MAJ79#11' or chord_type == '+M9#11' \
        or chord_type == '+M79#11' or chord_type == '+maj79#11' or chord_type == '+Maj79#11':
          type_ind = 107
        elif chord_type == 'AugMAJ79#11#' or chord_type == 'AugM9#11#' or chord_type == 'AugM79#11#' \
        or chord_type == 'Augmaj79#11#' or chord_type == 'AugMaj79#11#' or chord_type == 'augMAJ79#11#' \
        or chord_type == 'augM9#11#' or chord_type == 'augM79#11#' or chord_type == 'augmaj79#11#' \
        or chord_type == 'augMaj79#11#' or chord_type == '+MAJ79#11#' or chord_type == '+M9#11#' \
        or chord_type == '+M79#11#' or chord_type == '+maj79#11#' or chord_type == '+Maj79#11#':
          type_ind = 108
        elif chord_type == 'AugMAJ79#13' or chord_type == 'AugM9#13' or chord_type == 'AugM79#13' \
        or chord_type == 'Augmaj79#13' or chord_type == 'AugMaj79#13' or chord_type == 'augMAJ79#13' \
        or chord_type == 'augM9#13' or chord_type == 'augM79#13' or chord_type == 'augmaj79#13' \
        or chord_type == 'augMaj79#13' or chord_type == '+MAJ79#13' or chord_type == '+M9#13' \
        or chord_type == '+M79#13' or chord_type == '+maj79#13' or chord_type == '+Maj79#13':
          type_ind = 109
        elif chord_type == 'AugMAJ79b1113' or chord_type == 'AugM9b1113' or chord_type == 'AugM79b1113' \
        or chord_type == 'Augmaj79b1113' or chord_type == 'AugMaj79b1113' or chord_type == 'augMAJ79b1113' \
        or chord_type == 'augM9b1113' or chord_type == 'augM79b1113' or chord_type == 'augmaj79b1113' \
        or chord_type == 'augMaj79b1113' or chord_type == '+MAJ79b1113' or chord_type == '+M9b1113' \
        or chord_type == '+M79b1113' or chord_type == '+maj79b1113' or chord_type == '+Maj79b1113':
          type_ind = 110
        elif chord_type == 'AugMAJ79b11#13' or chord_type == 'AugM9b11#13' or chord_type == 'AugM79b11#13' \
        or chord_type == 'Augmaj79b11#13' or chord_type == 'AugMaj79b11#13' or chord_type == 'augMAJ79b11#13' \
        or chord_type == 'augM9b11#13' or chord_type == 'augM79b11#13' or chord_type == 'augmaj79b11#13' \
        or chord_type == 'augMaj79b11#13' or chord_type == '+MAJ79b11#13' or chord_type == '+M9b11#13' \
        or chord_type == '+M79b11#13' or chord_type == '+maj79b11#13' or chord_type == '+Maj79b11#13':
          type_ind = 111
        elif chord_type == 'AugMAJ791113' or chord_type == 'AugM91113' or chord_type == 'AugM791113' \
        or chord_type == 'Augmaj791113' or chord_type == 'AugMaj791113' or chord_type == 'augMAJ791113' \
        or chord_type == 'augM91113' or chord_type == 'augM791113' or chord_type == 'augmaj791113' \
        or chord_type == 'augMaj791113' or chord_type == '+MAJ791113' or chord_type == '+M91113' \
        or chord_type == '+M791113' or chord_type == '+maj791113' or chord_type == '+Maj791113':
          type_ind = 112
        elif chord_type == 'AugMAJ7911#13' or chord_type == 'AugM911#13' or chord_type == 'AugM7911#13' \
        or chord_type == 'Augmaj7911#13' or chord_type == 'AugMaj7911#13' or chord_type == 'augMAJ7911#13' \
        or chord_type == 'augM911#13' or chord_type == 'augM7911#13' or chord_type == 'augmaj7911#13' \
        or chord_type == 'augMaj7911#13' or chord_type == '+MAJ7911#13' or chord_type == '+M911#13' \
        or chord_type == '+M7911#13' or chord_type == '+maj7911#13' or chord_type == '+Maj7911#13':
          type_ind = 113
        elif chord_type == 'AugMAJ79#1113' or chord_type == 'AugM9#1113' or chord_type == 'AugM79#1113' \
        or chord_type == 'Augmaj79#1113' or chord_type == 'AugMaj79#1113' or chord_type == 'augMAJ79#1113' \
        or chord_type == 'augM9#1113' or chord_type == 'augM79#1113' or chord_type == 'augmaj79#1113' \
        or chord_type == 'augMaj79#1113' or chord_type == '+MAJ79#1113' or chord_type == '+M9#1113' \
        or chord_type == '+M79#1113' or chord_type == '+maj79#1113' or chord_type == '+Maj79#1113':
          type_ind = 114
        elif chord_type == 'AugMAJ79#11#13' or chord_type == 'AugM9#11#13' or chord_type == 'AugM79#11#13' \
        or chord_type == 'Augmaj79#11#13' or chord_type == 'AugMaj79#11#13' or chord_type == 'augMAJ79#11#13' \
        or chord_type == 'augM9#11#13' or chord_type == 'augM79#11#13' or chord_type == 'augmaj79#11#13' \
        or chord_type == 'augMaj79#11#13' or chord_type == '+MAJ79#11#13' or chord_type == '+M9#11#13' \
        or chord_type == '+M79#11#13' or chord_type == '+maj79#11#13' or chord_type == '+Maj79#11#13':
          type_ind = 115
        elif chord_type == 'AugMAJ7' or chord_type == 'AugM' or chord_type == 'AugM7' \
        or chord_type == 'Augmaj7' or chord_type == 'AugMaj7' or chord_type == 'augMAJ7' \
        or chord_type == 'augM' or chord_type == 'augM7' or chord_type == 'augmaj7' \
        or chord_type == 'augMaj7' or chord_type == '+MAJ7' or chord_type == '+M' \
        or chord_type == '+M7' or chord_type == '+maj7' or chord_type == '+Maj7':
          type_ind = 116
        elif chord_type == 'dim7' or chord_type == 'd7' or \
        chord_type == 'o7':
            type_ind = 117
        elif chord_type == 'dim79' or chord_type == 'd79' or \
        chord_type == 'o79':
            type_ind = 118
        elif chord_type == 'dim79#' or chord_type == 'd79#' or \
        chord_type == 'o79#':
            type_ind = 119
        elif chord_type == 'dim711' or chord_type == 'd711' or \
        chord_type == 'o711':
            type_ind = 120
        elif chord_type == 'dim7911' or chord_type == 'd911' or \
        chord_type == 'o911':
            type_ind = 121
        elif chord_type == 'dim79#11' or chord_type == 'd79#11' or \
        chord_type == 'o79#11':
            type_ind = 122
        elif chord_type == 'dim7913' or chord_type == 'd7913' or \
        chord_type == 'o7913':
            type_ind = 123
        elif chord_type == 'dim79#13' or chord_type == 'd79#13' or \
        chord_type == 'o79#13':
            type_ind = 124
        elif chord_type == 'dim71113' or chord_type == 'd71113' or \
        chord_type == 'o71113':
            type_ind = 125
        elif chord_type == 'dim791113' or chord_type == 'd791113' or \
        chord_type == 'o791113':
            type_ind = 126
        elif chord_type == 'dim79#1113' or chord_type == 'd9#71113' or \
        chord_type == 'o79#1113':
            type_ind = 127
        #TODO: take care of half-diminished symbol
        elif chord_type == 'm7b5':
            type_ind = 128
        elif chord_type == 'm7b59':
            type_ind = 129
        elif chord_type == 'm7b59#':
            type_ind = 130
        elif chord_type == 'm7b511':
            type_ind = 131
        elif chord_type == 'm7b513b':
            type_ind = 132
        elif chord_type == 'm7b5911':
            type_ind = 133
        elif chord_type == 'm7b5913b':
            type_ind = 134
        elif chord_type == 'm7b59#11':
            type_ind = 135
        elif chord_type == 'm7b59#13b':
            type_ind = 136
        elif chord_type == 'm7b51113b':
            type_ind = 137
        elif chord_type == 'm7b591113b':
            type_ind = 138
        elif chord_type == 'm7b59#1113':
            type_ind = 139
        elif chord_type == 'sus4' or chord_type == '4':
            type_ind = 140
        elif chord_type == 'sus2' or chord_type == '2':
            type_ind = 141
        else:
          return 0

        return root_ind * bass_ind * poss_chords_combs_num + type_ind + 1

    def encode(self, input, max_input_length):
        ans = {'input_ids':[], 'token_type_ids':[], 'attention_mask':[]}
        for chords in input:
            chords = chords.split()
            tokens = [0]
            i=2
            for chord in chords:
                i+=1
                tokens.append(self.tokenize(chord))
            tokens.append(0)
            padding = [0] * (max_input_length - i)
            ans['input_ids'].append(tokens + padding)
            ans['token_type_ids'].append([0 for _ in range(len(tokens))] + padding)
            ans['attention_mask'].append([1 for _ in range(len(tokens))] + padding)
        return ans

