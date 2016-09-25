""" Given a set of control points c_ij, computes and plots the corresponding
bezier surface over a given parameter domain R, a rectangle. """

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# control points
CP = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    [3, 2, 1]
])

fig = plt.figure()
axe = fig.add_subplot(111, projection='3d')

axe.scatter3D(CP[:, 0], CP[:, 1], CP[:, 2])

def decasteljau(control_points, u, v):
    m, n = control_points.shape

    # rows for u
    while m != 1:
        temp = np.ndarray((m-1, n))
        for j in range(n):
            for i in range(m-1):
                temp[i, j] = u * control_points[i, j] + (1 - u)*control_points[i+1, j]
        m = m - 1 
        control_points = temp
    control_points = control_points[0, :]
    
    # columns for v
    while n != 1:
        temp = np.zeros(n-1)
        for i in range(n-1):
            temp[i] = v*control_points[i] + (1 - v)*control_points[i+1]
        n = n - 1
        control_points = temp

    return control_points[0]

n = 10
u = np.linspace(0, 1, n)
v = np.linspace(0, 1, n)
surface_points = np.zeros(shape=(n, n))

for i, u_val in enumerate(u):
    for j, v_val in enumerate(v):
        surface_points[i, j] = decasteljau(CP, u_val, v_val)

u, v = np.meshgrid(u, v)
axe.plot_surface(u, v, surface_points)
plt.show()
