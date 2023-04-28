import numpy as np


class Piano:
    def __init__(self):
        self.sample_rate = 44100
        self.amplitude = 8192
        self.factor = [0.73, 0.16, 0.06, 0.01, 0.02, 0.01, 0.01]
        self.decay = [0.05, 0.02, 0.005, 0.1]
        self.sustain_level = 0.1

    def get_sine_wave(self, frequency: int, duration: float, amplitude: float) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sample_rate*duration))
        wave = self.amplitude*np.sin(2*np.pi*frequency*t)
        return wave

    def apply_overtones(self, frequency: int, duration: float, factor: list) -> np.ndarray:
        assert abs(1-sum(factor)) < 1e-8

        frequencies = np.minimum(
            np.array([frequency*(x+1) for x in range(len(factor))]), self.sample_rate//2)
        amplitudes = np.array([self.amplitude*x for x in factor])

        fundamental = self.get_sine_wave(
            frequencies[0], duration, amplitudes[0])
        for i in range(1, len(factor)):
            overtone = self.get_sine_wave(
                frequencies[i], duration, amplitudes[i])
            fundamental += overtone
        return fundamental

    def get_adsr_weights(self, frequency: int, duration: float, length: float, decay: list, sustain_level: float) -> np.ndarray:
        assert abs(sum(length)-1) < 1e-8
        assert len(length) == len(decay) == 4

        intervals = int(duration*frequency) + 1
        len_A = np.maximum(int(intervals*length[0]), 1)
        len_D = np.maximum(int(intervals*length[1]), 1)
        len_S = np.maximum(int(intervals*length[2]), 1)
        len_R = np.maximum(int(intervals*length[3]), 1)

        decay_A = decay[0]
        decay_D = decay[1]
        decay_S = decay[2]
        decay_R = decay[3]

        A = 1/np.array([(1-decay_A)**n for n in range(len_A)])
        A = A/np.nanmax(A)
        D = np.array([(1-decay_D)**n for n in range(len_D)])
        D = D*(1-sustain_level)+sustain_level
        S = np.array([(1-decay_S)**n for n in range(len_S)])
        S = S*sustain_level
        R = np.array([(1-decay_R)**n for n in range(len_R)])
        R = R*S[-1]

        weights = np.concatenate((A, D, S, R))
        smoothing = np.array([0.1*(1-0.1)**n for n in range(5)])
        smoothing = smoothing/np.nansum(smoothing)
        weights = np.convolve(weights, smoothing, mode='same')

        weights = np.repeat(weights, int(self.sample_rate*duration/intervals))
        tail = int(self.sample_rate*duration-weights.shape[0])
        if tail > 0:
            weights = np.concatenate(
                (weights, weights[-1]-weights[-1]/tail*np.arange(tail)))
        return weights

    def get_song_data(self, frequencies: list, note_values: list, length: list):
        duration = int(sum(note_values)*self.sample_rate)
        end_idx = np.cumsum(np.array(note_values)*self.sample_rate).astype(int)
        start_idx = np.concatenate(([0], end_idx[:-1]))
        end_idx = np.array([start_idx[i]+note_values[i] *
                           self.sample_rate for i in range(len(note_values))]).astype(int)

        song = np.zeros((duration,))
        for i in range(len(frequencies)):
            this_note = self.apply_overtones(
                frequencies[i], note_values[i], self.factor)
            weights = self.get_adsr_weights(frequencies[i], note_values[i], length,
                                            self.decay, self.sustain_level)
            new_note = this_note*weights
            if new_note.shape[0] == len(song[start_idx[i]:end_idx[i]] ):
                song[start_idx[i]:end_idx[i]] += this_note*weights
            else:
                song[start_idx[i]-1:end_idx[i]] += this_note*weights

        song = song*(self.amplitude/np.max(song))
        return song
