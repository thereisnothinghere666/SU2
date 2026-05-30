import numpy as np
import matplotlib.pyplot as plt

from acoustics.observers import create_observers
from acoustics.fwh import FWHSolver
from acoustics.spl import spl
from acoustics.fft_tools import spectrum
from acoustics.loader_history import load_history

dt = 5e-4

surface, pressure = load_history(
    "data/flow"
)

solver = FWHSolver(surface)

observers = create_observers(
    radius=10.0,
    n=10
)

all_spl = []

for obs in observers:

    signal = solver.pressure_signal(
        obs,
        pressure,
        dt
    )

    level = spl(signal)

    all_spl.append(level)

    freq, spec = spectrum(
        signal,
        dt
    )

    plt.figure()

    plt.plot(freq, spec)

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("SPL [dB]")

    plt.savefig(
        f"results/spec_{obs[0]:.1f}_{obs[1]:.1f}.png"
    )

plt.figure()

angles = np.linspace(
    0,
    2*np.pi,
    len(all_spl),
    endpoint=False
)

ax = plt.subplot(
    projection="polar"
)

ax.plot(
    angles,
    all_spl
)

plt.savefig(
    "results/directivity.png"
)