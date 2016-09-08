""" Given a set of control points c_ij, computes and plots the corresponding
bezier surface over a given parameter domain R, a rectangle. """
import numpy as np
from de_casteljau import decasteljau

control_points = np.array([
    [1, 3, 5],
    [2, 5, 1],
    [0, 1, 3]
    ])

print decasteljau(control_points, 1,1)
