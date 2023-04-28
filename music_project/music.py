from notes import get_piano_notes_88
from chord import get_major_chord_88
from guitar import Guitar
from piano import Piano
from fractals import Music

from scipy.io.wavfile import write
import numpy as np


l_mus = Music("F--F--F",  step=7, length=100)
l_mus.add_rules(("F", "F+F--F--F+F+"))
l_mus.generate_path(n_iter=4)
l_mus.music_path(45, 7)

piano = Piano()
result = 0
volume = 16384
notes_freq = get_piano_notes_88()
time = [0.01, 0.29, 0.6, 0.1]

print('start_piano')
for floor in range(len(l_mus.notes)):
    print('step')
    notes = np.array(l_mus.notes[floor]).reshape(len(l_mus.notes[floor])*2)
    freq = np.array([notes[x] for x in range(len(notes)) if x % 2 == 0])
    lenght = np.array([notes[x] for x in range(len(notes)) if x % 2 != 0])

    wave = piano.get_song_data(freq, lenght, time)
    wave = wave if wave.shape[0] % 10 == 0 else np.append(wave, 0)
    result += wave * (volume/np.max(wave))
    volume /= 2
write('fractal3.wav', 44100, result.astype(np.int16))
print('start_guitar_chord')
guitar = Guitar()
step = l_mus.axiom.count("F")*l_mus.rules['F'][0].count("F")
guitar_chord = []
for note in range(0, len(l_mus.notes[-1]), step):
    frequency = l_mus.notes[-1][note][0]
    duration = np.round(l_mus.notes[-1][note][1]*step, 4)
    this_note = list(notes_freq.keys())[list(
        notes_freq.values()).index(frequency)]
    index_note = list(notes_freq).index(this_note)
    chords = list(get_major_chord_88(index_note-12).values())
    random = np.random.randint(len(chords))
    chords = chords[random]
    tmp = 0

    for chord_note in chords:
        sound = guitar.guitarString(
            frequency=chord_note, duration=duration, volume=4096, toType=True)
        tmp += sound
    guitar_chord.append(tmp)

guitar_chord = guitar.normalizeData(
    guitar_note=guitar_chord, shape=result.shape[0])
result += guitar_chord

print('start_guitar_solo')
guitar_solo = []
for note in range(len(l_mus.notes[-1])):
    frequency = l_mus.notes[-1][note][0]
    duration = l_mus.notes[-1][note][1]
    sound = guitar.guitarString(
        frequency=frequency, duration=duration, volume=2048, toType=True)
    guitar_solo.append(sound)

guitar_solo = guitar.normalizeData(
    guitar_note=guitar_solo, shape=result.shape[0])
result += guitar_solo

write('fractal2.wav', 44100, result.astype(np.int16))
print('succesfull')
