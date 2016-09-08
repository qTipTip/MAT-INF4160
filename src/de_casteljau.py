"""
Given an (m x n)-matrix of controlpoints c_ij and two parameters u, v,
computes the value of the Bezier surface with controlpoints c_ij at the
point (u, v).

Notice that u, v is typically parametrized by s, t in some arbitrary
parameter rectangle [a1, b1]x[a2, b2]
"""

import numpy as np

def decasteljau(control_points, u, v):
    """
    Given an (m x n)-matrix of controlpoints c_ij and two parameters u, v,
    computes the value of the Bezier surface with controlpoints c_ij at the
    point (u, v).

    Notice that u, v is typically parametrized by s, t in some arbitrary
    parameter rectangle [a1, b1]x[a2, b2] where u, v end up in the unit square
    [0, 1]x[0, 1]
    """

    m, n = control_points.shape
    
    # De Casteljau with respect to u. The matrix is reduced by one row each
    # iteration
    while m != 1: 
        temp = np.ndarray((m-1, n))
        for j in range(n):
            for i in range(m - 1):
                temp[i, j] = u * control_points[i, j] + (1 - u)*control_points[i+1, j]
        m = m - 1
        control_points = temp

    control_points = control_points[0,:] # casting to one-dim array
    # De Casteljau with respect to v.  The array is reduced by one column each
    # iteration
    while n != 1:
        temp = np.zeros(n-1)
        for i in range(len(temp)):
            temp[i] = v * control_points[i] + (1 - v)*control_points[i+1]
        n = n - 1
        control_points = temp 

    # The value of p(u, v) is then
    return control_points[0]

if __name__ == "__main__":

    control_points = np.array([
        [0, 0, 0, 6],
        [18, 2, 0, 8],
        [4, 0, 4, 18]
        ])
    print decasteljau(control_points, 0.5, 2./3)
