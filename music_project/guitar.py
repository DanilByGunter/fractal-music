import numpy as np


class Guitar:
    def guitarString(self, frequency: float, duration=1., sample_rate=44100, volume=32767, p=0.5, beta=0.6, S=0.8, C=0.5, L=0.5, toType=False) -> np.ndarray:
        N = int(sample_rate/frequency) if frequency != 0 else 1

        noise = np.random.uniform(-1, 1, N)

        buffer = np.zeros_like(noise)
        buffer[0] = (1 - p) * noise[0]
        for i in range(1, N):
            buffer[i] = (1-p)*noise[i] + p*buffer[i-1]
        noise = buffer

        pick = int(beta*N+1/2)
        if pick == 0:
            pick = N
        buffer = np.zeros_like(noise)
        for i in range(N):
            if i-pick < 0:
                buffer[i] = noise[i]
            else:
                buffer[i] = noise[i]-noise[i-pick]
        noise = buffer

        samples = np.zeros(int(sample_rate*duration))
        for i in range(N):
            samples[i] = noise[i]*0.5

        def delayLine(n): return samples[n-N]

        def stringDampling_filter(n): return 0.992 * \
            ((1-S)*delayLine(n)+S*delayLine(n-1))

        def firstOrder_stringTuning_allpass_filter(
            n): return C*(stringDampling_filter(n)-samples[n-1])+stringDampling_filter(n-1)

        for i in range(N, len(samples)):
            samples[i] = firstOrder_stringTuning_allpass_filter(i)

        w_tilde = np.pi*frequency/sample_rate
        buffer = np.zeros_like(samples)
        buffer[0] = w_tilde/(1+w_tilde)*samples[0]
        for i in range(1, len(samples)):
            buffer[i] = w_tilde/(1+w_tilde)*(samples[i] +
                                             samples[i-1])+(1-w_tilde)/(1+w_tilde)*buffer[i-1]
        samples = (L**(4/3)*samples)+(1.0-L)*buffer
        if toType:
            samples = samples/np.max(np.abs(samples))
            return np.int16(samples*volume)
        else:
            return samples

    def normalizeData(self, guitar_note: np.ndarray, shape: int) -> np.ndarray:
        guitar_note = np.concatenate(guitar_note)
        count = shape - guitar_note.shape[0]
        step = int(guitar_note.shape[0] / count) if count != 0 else 0
        result = []
        if step != 0:
            for note in range(0, guitar_note.shape[0]):
                result.append(guitar_note[note])
                if note % step == 0:
                    result.append(0)
        return result if len(result) != 0 else guitar_note
