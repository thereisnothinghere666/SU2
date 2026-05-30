import pandas as pd
import numpy as np


class Snapshot:

    def __init__(self, filename):

        df = pd.read_csv(filename)

        self.x = df["x"].values
        self.y = df["y"].values

        self.p = df["Pressure"].values

        self.u = df["Velocity_X"].values
        self.v = df["Velocity_Y"].values