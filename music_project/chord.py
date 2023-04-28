from notes import get_piano_notes_88

notes = list(get_piano_notes_88())
frequencis = get_piano_notes_88()


def get_major_chord_88(note: float) -> dict:
    chords = dict()
    note = note if note+23 < 87 else note - 24
    chords['T53'] = [frequencis[notes[note]],
                     frequencis[notes[note+4]], frequencis[notes[note+7]]]
    chords['T6'] = [frequencis[notes[note+4]],
                    frequencis[notes[note+7]], frequencis[notes[note+12]]]
    chords['T64'] = [frequencis[notes[note+7]],
                     frequencis[notes[note+12]], frequencis[notes[note+16]]]
    chords['S53'] = [frequencis[notes[note+5]],
                     frequencis[notes[note+9]], frequencis[notes[note+12]]]
    chords['S6'] = [frequencis[notes[note+9]],
                    frequencis[notes[note+12]], frequencis[notes[note+17]]]
    chords['S64'] = [frequencis[notes[note+12]],
                     frequencis[notes[note+17]], frequencis[notes[note+21]]]
    chords['D53'] = [frequencis[notes[note+7]],
                     frequencis[notes[note+11]], frequencis[notes[note+14]]]
    chords['D6'] = [frequencis[notes[note+11]],
                    frequencis[notes[note+14]], frequencis[notes[note+19]]]
    chords['D64'] = [frequencis[notes[note+14]],
                     frequencis[notes[note+19]], frequencis[notes[note+23]]]
    return chords


def get_minor_chord_88(note: int) -> dict:
    chords = dict()
    chords['T53'] = [frequencis[notes[note]],
                     frequencis[notes[note+3]], frequencis[notes[note+7]]]
    chords['T6'] = [frequencis[notes[note+3]],
                    frequencis[notes[note+7]], frequencis[notes[note+12]]]
    chords['T64'] = [frequencis[notes[note+7]],
                     frequencis[notes[note+12]], frequencis[notes[note+15]]]
    chords['S53'] = [frequencis[notes[note+5]],
                     frequencis[notes[note+8]], frequencis[notes[note+12]]]
    chords['S6'] = [frequencis[notes[note+8]],
                    frequencis[notes[note+12]], frequencis[notes[note+17]]]
    chords['S64'] = [frequencis[notes[note+12]],
                     frequencis[notes[note+17]], frequencis[notes[note+20]]]
    chords['D53'] = [frequencis[notes[note+7]],
                     frequencis[notes[note+10]], frequencis[notes[note+14]]]
    chords['D6'] = [frequencis[notes[note+10]],
                    frequencis[notes[note+14]], frequencis[notes[note+19]]]
    chords['D64'] = [frequencis[notes[note+14]],
                     frequencis[notes[note+19]], frequencis[notes[note+22]]]
    return chords
