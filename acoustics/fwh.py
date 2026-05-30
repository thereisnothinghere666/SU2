import numpy as np


C0 = 343.0


class FWHSolver:

    def __init__(self,
                 surface_points):

        self.surface = surface_points

    def pressure_signal(
            self,
            observer,
            pressure_history,
            dt):

        nsteps = pressure_history.shape[0]

        signal = np.zeros(nsteps)

        for t in range(1, nsteps):

            p_now = pressure_history[t]
            p_prev = pressure_history[t-1]

            dpdt = (p_now - p_prev)/dt

            value = 0.0

            for i in range(len(self.surface)):

                xs = self.surface[i,0]
                ys = self.surface[i,1]

                dx = observer[0]-xs
                dy = observer[1]-ys

                r = np.sqrt(dx*dx + dy*dy)

                value += dpdt[i]/(4*np.pi*r)

            signal[t] = value

        return signal