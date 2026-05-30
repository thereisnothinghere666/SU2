import numpy as np


def spectrum(signal, dt):

    N = len(signal)

    fft = np.fft.rfft(signal)

    freq = np.fft.rfftfreq(
        N,
        dt
    )

    amp = np.abs(fft)

    spl = 20*np.log10(
        amp/np.max(amp)
    )

    return freq, spl