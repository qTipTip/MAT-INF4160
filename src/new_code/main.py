import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style

matplotlib.style.use('ggplot')

def make_knot_vector(d, n, curve_type='uniform'):
    """
    Creates a uniform knot vector of knots in the interval [0, n + d + 1]

    :d: order of basis functions
    :n: the number of control points / the number of basis functions
    :curve_type: the type of curve to model - [clamped/uniform]
    :returns: (t_1, t_2, ..., t_(n+d+1)) a knot vector
    """
    
    total_knots = d + n + 1
    outer_knots = d + 1
    inner_knots = total_knots - 2*outer_knots
    
    if curve_type == 'uniform':
        return range(total_knots)
    elif curve_type == 'clamped':
        knots = [0]*outer_knots
        knots += range(1, inner_knots + 1)
        knots += [inner_knots]*outer_knots
        return knots 
    else:
        raise NotImplementedError

def basis(t, i, knots, degree=0):
    """
    Returns the i'th zero-basis evaluated at t for the given knot vector
    """
    if degree == 0:
        if knots[i] <= t < knots[i+1]:
            return 1.0
        else:
            return 0.0
    else:
        result = 0
        denom_one = knots[i+degree] - knots[i]
        denom_two = knots[i+1+degree] - knots[i+1]    
        tol = 1.0E-14
        if abs(denom_one) > tol: 
            result += (t - knots[i]) / denom_one * basis(t, i, knots, degree-1)
        if abs(denom_two) > tol:
            result += (knots[i+1+degree] - t) / denom_two * basis(t, i + 1, knots, degree-1)
        return result

d = 2
n = 3
knots = make_knot_vector(d, n)
t_vals = np.linspace(knots[0], knots[-1], 1000)
for i in range(n):
    y_vals = [basis(t, i, knots, d) for t in t_vals]
    plt.plot(t_vals, y_vals, lw=3, alpha=0.8)
plt.axis(ymin=0, ymax=1.5)
plt.show()
