from multipledispatch import dispatch
from midiutil import MIDIFile
import pygame.midi as midi
import random as r
import time as t
import re


class Music:
    def __init__(self, axiom, step):
        self.axiom = axiom
        self.state = [axiom]
        self.step = step
        self.rules = {}
        self.key_re_list = []
        self.notes = []

    def add_rules(self, *rules):
        if len(rules[0][0]) >= 2:
            tmp = []
            for change in rules[0]:
                tmp.append(change)
            rules = tmp
        for key, value in rules:
            key_re = ""
            if not isinstance(value, str):
                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
                key_re = key_re.replace("+", r"\+")
                key_re = key_re.replace("-", r"\-")
                key_re = re.sub(
                    r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                self.key_re_list.append(key_re)
            self.rules[key] = (value, key_re)

    def update_param_cmd(self, m):
        if not self.function_key:
            return ""

        args = list(map(float, m.groups()))
        return self.function_key(*args).lower()

    def generate_path(self, n_iter):
        for n in range(n_iter):
            tmp = ''
            for key, values in self.rules.items():
                if isinstance(values[0], str):
                    tmp += self.state[n].replace(key, values[0].upper())
                else:
                    self.function_key = values[0]
                    self.state[n] = re.sub(
                        values[1], self.update_param_cmd, self.state)
                    self.function_key = None
            self.state.append(tmp)

    @dispatch(int, int)
    def music_path(self, first_note, coeff):
        for step in self.state:
            tmp_notes = []
            for symb in step:
                match symb:
                    case "F": tmp_notes.append(first_note)
                    case "+": first_note = round(first_note + self.step) if round(first_note + self.step) <= 96 else round(first_note - self.step) - 12
                    case "-": first_note = round(first_note - self.step) if round(first_note - self.step) >= 21 else round(first_note + self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step + self.step/coeff - 24)
        self.music_volume()

    @dispatch(int, int, int)
    def music_path(self, first_note, second_note, coeff):
        for step in self.state:
            tmp_notes = []
            last_note = ""
            for symb in step:
                last_note = symb if symb in "FX" else last_note
                match symb:
                    case "F": tmp_notes.append(first_note)
                    case "X": tmp_notes.append(second_note)
                    case "+":
                        if last_note == "F":
                            first_note = round(first_note + self.step) if round(
                                first_note + self.step) <= 96 else round(first_note + self.step) - 12
                        else:
                            second_note = round(second_note + self.step) if round(
                                second_note + self.step) <= 96 else round(second_note + self.step) - 12
                    case "-":
                        if last_note == "F":
                            first_note = round(first_note - self.step) if round(
                                first_note - self.step) >= 21 else round(first_note - self.step) + 12
                        else:
                            second_note = round(second_note - self.step) if round(
                                second_note - self.step) >= 21 else round(second_note - self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step - self.step/coeff)
        self.music_volume()

    @dispatch(int, int, int, int)
    def music_path(self, first_note, second_note, third_note, coeff):
        for step in self.state:
            tmp_notes = []
            for symb in step:
                last_note = symb if symb in "FXY" else last_note
                match symb:
                    case "F": tmp_notes.append(first_note)
                    case "X": tmp_notes.append(second_note)
                    case "X": tmp_notes.append(third_note)
                    case "+":
                        if last_note == "F":
                            first_note = round(first_note + self.step) if round(
                                first_note + self.step) <= 96 else round(first_note + self.step) - 12
                        elif last_note == "X":
                            second_note = round(second_note + self.step) if round(
                                second_note + self.step) <= 96 else round(second_note + self.step) - 12
                        else:
                            third_note = round(third_note + self.step) if round(
                                third_note + self.step) <= 96 else round(third_note + self.step) - 12
                    case "-":
                        if last_note == "F":
                            first_note = round(first_note - self.step) if round(
                                first_note - self.step) >= 21 else round(first_note - self.step) + 12
                        elif last_note == "X":
                            third_note = round(third_note - self.step) if round(
                                third_note - self.step) >= 21 else round(third_note - self.step) + 12
                        else:
                            third_note = round(third_note - self.step) if round(
                                third_note - self.step) >= 21 else round(third_note - self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step - self.step/coeff)
        self.music_volume()

    def music_volume(self):
        notes = []
        k = 0
        for step in self.notes:
            tmp = []
            for note in step:
                tmp.append([note, 127-15*k])
                for _ in range(len(self.notes[-1])//len(step)-1):
                    tmp.append([0, 0])
            notes.append(tmp)
            k += 1
        self.notes = notes


def play(len_note):
    midi.init()
    player = midi.Output(0)

    notes = l_mus.notes

    for x in range(len(notes[0])):
        player.set_instrument(1, 1)
        match count:
            case 1:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
            case 2:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
            case 3:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
            case 4:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
                player.note_on(notes[3][x][0], notes[3][x][1], 3)
            case 5:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
                player.note_on(notes[3][x][0], notes[3][x][1], 3)
                player.note_on(notes[4][x][0], notes[4][x][1], 8)
            case 6:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
                player.note_on(notes[3][x][0], notes[3][x][1], 3)
                player.note_on(notes[4][x][0], notes[4][x][1], 8)
                player.note_on(notes[5][x][0], notes[5][x][1], 8)
            case 7:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
                player.note_on(notes[3][x][0], notes[3][x][1], 3)
                player.note_on(notes[4][x][0], notes[4][x][1], 8)
                player.note_on(notes[5][x][0], notes[5][x][1], 8)
                player.note_on(notes[6][x][0], notes[6][x][1], 3)
            case 8:
                player.note_on(notes[0][x][0], notes[0][x][1], 15)
                player.note_on(notes[1][x][0], notes[1][x][1], 10)
                player.note_on(notes[2][x][0], notes[2][x][1], 1)
                player.note_on(notes[3][x][0], notes[3][x][1], 3)
                player.note_on(notes[4][x][0], notes[4][x][1], 8)
                player.note_on(notes[5][x][0], notes[5][x][1], 8)
                player.note_on(notes[6][x][0], notes[6][x][1], 3)
                player.note_on(notes[7][x][0], notes[7][x][1], 2)
        t.sleep(len_note)


def save(len_note, number):
    notes = l_mus.notes

    track = 0
    time = 0
    tempo = 60
    MyMIDI = MIDIFile(1)

    MyMIDI.addTempo(track, time, tempo)
    for x in range(len(notes[0])):
        match count:
            case 1:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
            case 2:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
            case 3:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
            case 4:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
                MyMIDI.addNote(track, 3, notes[3]
                               [x][0], time, 3, notes[3][x][1])
            case 5:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
                MyMIDI.addNote(track, 3, notes[3]
                               [x][0], time, 3, notes[3][x][1])
                MyMIDI.addNote(track, 8, notes[4]
                               [x][0], time, 8, notes[4][x][1])
            case 6:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
                MyMIDI.addNote(track, 3, notes[3]
                               [x][0], time, 3, notes[3][x][1])
                MyMIDI.addNote(track, 8, notes[4]
                               [x][0], time, 8, notes[4][x][1])
                MyMIDI.addNote(track, 8, notes[5]
                               [x][0], time, 8, notes[5][x][1])
            case 7:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
                MyMIDI.addNote(track, 3, notes[3]
                               [x][0], time, 3, notes[3][x][1])
                MyMIDI.addNote(track, 8, notes[4]
                               [x][0], time, 8, notes[4][x][1])
                MyMIDI.addNote(track, 8, notes[5]
                               [x][0], time, 8, notes[5][x][1])
                MyMIDI.addNote(track, 3, notes[6]
                               [x][0], time, 3, notes[6][x][1])
            case 8:
                MyMIDI.addNote(
                    track, 15, notes[0][x][0], time, 15, notes[0][x][1])
                MyMIDI.addNote(
                    track, 10, notes[1][x][0], time, 10, notes[1][x][1])
                MyMIDI.addNote(track, 1, notes[2]
                               [x][0], time, 1, notes[2][x][1])
                MyMIDI.addNote(track, 3, notes[3]
                               [x][0], time, 3, notes[3][x][1])
                MyMIDI.addNote(track, 8, notes[4]
                               [x][0], time, 8, notes[4][x][1])
                MyMIDI.addNote(track, 8, notes[5]
                               [x][0], time, 8, notes[5][x][1])
                MyMIDI.addNote(track, 3, notes[6]
                               [x][0], time, 3, notes[6][x][1])
                MyMIDI.addNote(track, 2, notes[7]
                               [x][0], time, 2, notes[7][x][1])
        time = time + len_note

    with open(f"fractal{number}.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


axioms = ["F--F--F", "F+F+F+F", "F--F", "F-F-F-F", "F",
          "YF", "FXF--FF--FF", "F+F+F+F", "F+F+F+F", "F+F+F+F", "F+F+F+F",
          "F++F++F++F++F", "FX", "F+XF+F+XF", "-X--X", "X",
          "F", "F+F+F+F", "F+F+F", "FX", "F", "FX+FX", "FX+FX+FX"]
rules = [("F", "F+F--F+F"),
         ("F", "FF+F++F+F"), ("F", "F-F+F+F-F"), ("F", "F-F+F+F-F"), ("F", "+F--F+"),
         (("X", "YF+XF+Y"), ("Y", "XF-YF-X")),
         (("F", "FF"), ("X", "--FXF++FXF++FXF--")), ("F", "FF+F+F+F+FF"),
         ("F", "FF+F-F+F+FF"), ("F", "FF+F+F+F+F+F-F"), ("F", "F+F-F+F+F"),
         ("F", "F++F++F+++++F-F++F"), (("X", "X+YF++YF-FX--FXFX-YF+"),
                                       ("Y", "-FX+YFYF++YF+FX--FX-Y")),
         ("X", "XF-F+F-XF+F+XF-F+F-X"), ("X", "XFX--XFX"),
         (("X", "XFYFX+F+YFXFY-F-XFYFX"), ("Y", "YFXFY-F-XFYFX+F+YFXFY")),
         ("F", "F+F-F-F-F+F+F+F-F"), ("F", "F+FF++F+F"), ("F", "F-F+F"),
         (("X", "X+YF+"), ("Y", "-FX-Y")), ("F", "F-F+F"),
         (("X", "X+YF+"), ("Y", "-FX-Y")), (("X", "X+YF+"), ("Y", "-FX-Y"))]
count = 5
coeff = 2
number = 0

for axiom, rule in zip(axioms, rules):
    for _ in range(5):
        print(number)

        steps = [4, 5, 7, 9, 12]
        notes_choice = [51, 55, 59, 60, 61]

        step = r.choice(steps)
        note = r.choice(notes_choice)

        l_mus = Music(axiom,  step)
        l_mus.add_rules(rule)
        l_mus.generate_path(count)
        if "Y" in set(rule):
            l_mus.music_path(note, note + 4, note - 4, coeff)
        elif "X" in set(rule):
            l_mus.music_path(note, note + 4, coeff)
        else:
            l_mus.music_path(note, coeff)

        sec = r.randint(0, 5)
        save(0.07 - sec/100, number)

        number += 1
