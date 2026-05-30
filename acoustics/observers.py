import numpy as np


def create_observers(
        radius=10.0,
        n=10):

    theta = np.linspace(
        0,
        2*np.pi,
        n,
        endpoint=False
    )

    obs = np.zeros((n, 2))

    obs[:,0] = radius*np.cos(theta)
    obs[:,1] = radius*np.sin(theta)

    return obs