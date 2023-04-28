from multipledispatch import dispatch
from notes import get_piano_notes_88
import re


class Music:
    def __init__(self, axiom: str, step: int, length: int):
        self.axiom = axiom
        self.state = [axiom]
        self.step = step
        self.rules = {}
        self.key_re_list = []
        self.notes = []
        self.length = length

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

    def generate_path(self, n_iter: int):
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
    def music_path(self, first_note: int, coeff: int):
        for step in self.state:
            tmp_notes = []
            for symb in step:
                match symb:
                    case "F": tmp_notes.append(first_note)
                    case "+": first_note = round(first_note + self.step) if round(first_note + self.step) <= 87 else round(first_note - self.step) - 12
                    case "-": first_note = round(first_note - self.step) if round(first_note - self.step) >= 0 else round(first_note + self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step + self.step/coeff - 24)
        self.music()

    @dispatch(int, int, int)
    def music_path(self, first_note: int, second_note: int, coeff: int):
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
                                first_note + self.step) <= 87 else round(first_note + self.step) - 12
                        else:
                            second_note = round(second_note + self.step) if round(
                                second_note + self.step) <= 87 else round(second_note + self.step) - 12
                    case "-":
                        if last_note == "F":
                            first_note = round(first_note - self.step) if round(
                                first_note - self.step) >= 0 else round(first_note - self.step) + 12
                        else:
                            second_note = round(second_note - self.step) if round(
                                second_note - self.step) >= 0 else round(second_note - self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step - self.step/coeff)
        self.music()

    @dispatch(int, int, int, int)
    def music_path(self, first_note: int, second_note: int, third_note: int, coeff: int):
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
                                first_note + self.step) <= 87 else round(first_note + self.step) - 12
                        elif last_note == "X":
                            second_note = round(second_note + self.step) if round(
                                second_note + self.step) <= 87 else round(second_note + self.step) - 12
                        else:
                            third_note = round(third_note + self.step) if round(
                                third_note + self.step) <= 87 else round(third_note + self.step) - 12
                    case "-":
                        if last_note == "F":
                            first_note = round(first_note - self.step) if round(
                                first_note - self.step) >= 0 else round(first_note - self.step) + 12
                        elif last_note == "X":
                            third_note = round(third_note - self.step) if round(
                                third_note - self.step) >= 0 else round(third_note - self.step) + 12
                        else:
                            third_note = round(third_note - self.step) if round(
                                third_note - self.step) >= 0 else round(third_note - self.step) + 12
            self.notes.append(tmp_notes)
            self.step = (self.step + self.step/coeff) if (self.step +
                                                          self.step/coeff) <= 24 else (self.step - self.step/coeff)
        self.music()

    def music(self):
        notes = []
        notes_freq = list(get_piano_notes_88())
        frequencis = get_piano_notes_88()
        length = self.length
        for step in self.notes:
            tmp = []
            for note in step:
                note_freq = frequencis[notes_freq[note]]
                tmp.append([note_freq, length])
                for _ in range(len(self.notes[-1])//len(step)-1):
                    tmp.append([0, 0])
            notes.append(tmp)
            length /= self.rules['F'][0].count("F")
        self.notes = notes
