import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style
matplotlib.style.use('fivethirtyeight')
class CompositeBezierCurve():
    """
    Represents a composite Bezier Curve
    input:
    :curve_segments: a list of BezierCurve objects
    :knots: a list of parameter domains, where each segment is defined
    e.g., [0, 1, 2], curve_segments[0] defined on 0, 1, curve_segments[1] defined on [1, 2]
    """
    def __init__(self, curve_segments, knots, label='C'):
        self.curves = curve_segments
        self.K = knots  
        self.C = np.concatenate([c.C for c in self.curves])
        self.label = label
        self.sublabels = [c.label for c in curve_segments]
    
    def __call__(self, t):
        for i in range(len(self.K)-1):
            if self.K[i] <= t < self.K[i+1]:
                break
        return self.curves[i](t)

    def plot(self, resolution=50):
        t_values = np.linspace(self.K[0], self.K[-1], resolution)
        y_values = [self(t) for t in t_values]
        plt.plot(*zip(*y_values), label='$[\\,' + ';\\;\\;'.join(l for l in self.sublabels) + '\\,]$')
        plt.scatter(*zip(*self.C))
        plt.plot(*zip(*self.C), alpha=0.3, lw=2, color='grey')

    def __str__(self):
        return """
        %s is a piecewise polynomial defined by
        %s
        """ % (self.label, '\n'.join(str(c) for c in self.curves))


class BezierCurve():
    """
    input:
    :a: lower parameter limit
    :b: upper parameter limit
    :C: set of control points
    """

    def __init__(self, control_points, a = 0, b = 1, label=''):
        self.a = a
        self.b = b
        self.C = np.array(control_points)
        self.n = self.C.shape[0]
        self.label = label
        try:
            self.D = self.C.shape[1]
        except:
            self.D = 1

    def __call__(self, t):
        a, b = self.a, self.b
        u = (t - a) / float(b - a)
        n = self.n
        prev = self.C
        for r in range(1, n):
            new = np.zeros((n-r, self.D))
            for i in range(len(prev)-1):
                new[i] = (1 - u)*prev[i] + u*prev[i+1]
            prev = new
        return prev[0]
   
    
    def plot(self, resolution=50):
        plt.scatter(*zip(*self.C))
        plt.plot(*zip(*self.C), alpha=0.3, lw=2, color='grey')
        t_vals = np.linspace(self.a, self.b, resolution)
        curve  = [self(t) for t in t_vals]
        plt.plot(*zip(*curve), label='$'+self.label+'$', lw=3)
    
    def __str__(self):
        return """
        %s defined on [%d, %d] 
        """ % (self.label, self.a, self.b)

if __name__ == "__main__":
    control_points_p = [(-1, 1), (-1, 0), (0, 0)]
    control_points_q = [(0, 0), (1, 0), (2, 1)]
    p = BezierCurve(a=0, b = 1, control_points=control_points_p, label='p(t)')
    q = BezierCurve(a = 1, b = 2, control_points=control_points_q, label='q(t)')
    comp = CompositeBezierCurve([p, q], [0, 1, 2], label='C(t)')
    comp.plot(20)
    plt.legend(loc='best')
    plt.show()
    print comp
