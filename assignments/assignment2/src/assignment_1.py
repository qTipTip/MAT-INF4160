from bezier_lib import BezierCurve, CompositeBezierCurve

p_points = [(-1, 1), (-1, 0), (0, 0)]
q_points = [(0, 0), (1, 0), (2, 1)]

p = BezierCurve(p_points, a=0, b=1, label='p(t)')
q = BezierCurve(q_points, a=1, b=2, label='q(t)')
s = CompositeBezierCurve([p, q], (0, 1, 2), label='s(t)')

s.plot(resolution=500, display=True)
