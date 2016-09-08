import matplotlib.pyplot as plt
import numpy as np

def B_3(i, x):
    if i == 0:
        return (1 - x)**3
    elif i == 1:
        return 3*x*(1 - x)**2
    elif i == 2:
        return 3*x**2*(1-x)
    else:
        return x**3

def f(x):
    return x**3 - 2*x**2 - 3*x + 12

def f2(x):
    return x**2 if x < 0.5 else 2*x 

def g(f, x, n=3):
    return sum([f(float(i) / n) * B_3(i, x) for i in range(n+1)])

x_vals = np.linspace(0, 1, 1000)
f2_vals = [f2(x) for x in x_vals]
plt.plot(x_vals, f2_vals)
plt.plot(x_vals, g(f2, x_vals))
plt.show()
