import numpy as np

P_REF = 20e-6


def spl(signal):

    rms = np.sqrt(
        np.mean(signal**2)
    )

    return 20*np.log10(
        rms/P_REF
    )