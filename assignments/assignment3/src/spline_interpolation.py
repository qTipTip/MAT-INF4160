import numpy as np
from bezier_lib import *
# given:

x_values = np.array([(0, 1, 2), (2, 3, 5), (3, 1, 1), (4, 10, 8), (3, 50, 1), (5, 10, 2)])
n = len(x_values)

# chose

t_values = np.linspace(0, 1, n)

print x_values
print t_values

# c_1 continuity first
# compute derivatives
m_values = []
m_values.append((x_values[1] - x_values[0]) / (t_values[1] - t_values[0]))
for i in range(1, n-1):
    h_i = t_values[i+1] - t_values[i]
    m_values.append((x_values[i+1] - x_values[i]) / h_i)
m_values.append((x_values[-1] - x_values[-2]) / t_values[-1] - (t_values[-2]))

curve_segments = []
knots = [t_values[0]]
# compute control points for each spline
for i in range(n-1):
    h_i = t_values[i+1] - t_values[i]
    CP = []  
    CP.append(x_values[i])
    CP.append(x_values[i] + h_i * m_values[i] / 3)
    CP.append(x_values[i+1] - h_i * m_values[i+1] / 3)
    CP.append(x_values[i+1])
    curve = BezierCurve(CP, t_values[i], t_values[i+1], label='s_%d' % i)
    curve_segments.append(curve)
    knots.append(t_values[i+1])
curve = CompositeBezierCurve(curve_segments, knots)
fig = curve.plot(display=False)
ax = fig.gca()
ax.scatter(*zip(*x_values), s=100, zorder=10)
plt.show()
