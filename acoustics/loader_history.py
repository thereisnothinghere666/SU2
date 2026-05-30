import glob
import numpy as np

from acoustics.loader import Snapshot


def load_history(path):

    files = sorted(
        glob.glob(path + "/*.csv")
    )

    pressure = []
    surface = None

    for f in files:

        snap = Snapshot(f)

        pressure.append(snap.p)

        if surface is None:

            surface = np.column_stack(
                [snap.x, snap.y]
            )

    pressure = np.array(pressure)

    return surface, pressure