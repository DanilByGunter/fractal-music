import numpy as np


def get_piano_notes_88() -> dict:
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    base_freq = 440
    keys = np.array([x+str(y) for y in range(0, 9) for x in octave])

    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]

    note_freqs = dict(
        zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0

    return note_freqs


def get_piano_notes_176() -> dict:
    octave = ['C', 'Cc', 'c', 'cD', 'D', 'Dd',
              'd', 'dE', 'E', 'EF', 'F', 'Ff', 'f', 'fG', 'G', 'Gg',
              'g', 'gA', 'A', 'Aa', 'a', 'aB', 'B', 'BC']
    base_freq = 440
    keys = np.array([x+str(y) for y in range(0, 9) for x in octave])
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]

    note_freqs = dict(
        zip(keys, [2**((n+2-98)/24)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0

    return note_freqs


def get_piano_notes_352() -> dict:
    octave = ['C', 'CCc', 'Cc', 'Ccc', 'c', 'ccD', 'cD', 'cDD', 'D', 'DDd', 'Dd', 'Ddd',
              'd', 'ddE', 'dE', 'dEE', 'E', 'EEF', 'EF', 'EFF', 'F', 'FFf', 'Ff', 'Fff', 'f', 'ffG', 'fG', 'fGG', 'G', 'GGg', 'Gg', 'Ggg',
              'g', 'ggA', 'gA', 'gAA', 'A', 'AAa', 'Aa', 'Aaa', 'a', 'aaB', 'aB', 'aBB', 'B', 'BBC', 'BC', 'BCC']
    base_freq = 440
    keys = np.array([x+str(y) for y in range(0, 9) for x in octave])
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]

    note_freqs = dict(
        zip(keys, [2**((n+4-196)/48)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0

    return note_freqs
