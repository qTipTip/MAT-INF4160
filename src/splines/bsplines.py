import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

class BSpline(object):

    """
    Inputs:
        knot_vector: list or array containing the knots
        order: order of interpolation. order 0 gives piecewise constant
                                       order 1 gives piecewise linear,
                                       etc.

    Outputs:
        callable object to evaluate basis functions    
    """

    def __init__(self, knot_vector, order):

        self.knot_vector = np.array(knot_vector, dtype=float)
        self.order = order
    
    def __call__(self, u):
        """
        Evaluates the basis functions at the point u
        """
        return self.__compute_basis(u, self.order)

    def __compute_zero_basis(self, u):
        """
        The basis of order zero. Used for recursively computing the basis
        vectors of higher degree.

        Returns the value of each basis element at u, either zero or one.
        """ 
        
        return np.where(np.all([self.knot_vector[:-1] <=  u, u < self.knot_vector[1:]],axis=0), 1.0, 0.0)
        """ does not work for some reason
        lower_mask = ma.masked_less_equal(self.knot_vector[:-1], u).mask 
        upper_mask = ma.masked_greater(self.knot_vector[1:], u).mask
        
        return np.where(np.all([lower_mask, upper_mask], axis=0), 1.0, 0.0)
        """

    def __compute_basis(self, u, order):
    
        # if the interpolation is constant, return the zero basis
        if order == 0:
            return self.__compute_zero_basis(u)

        # else compute the basis elements of lower order
        else:
            previous_basis = self.__compute_basis(u, order-1)

        # evaluate the recurrence relation computing the whole column
        # in the triangular scheme at once
        first_term_numerator = u - self.knot_vector[:-order]
        first_term_denominator = self.knot_vector[order:] - self.knot_vector[:-order]

        second_term_numerator = self.knot_vector[(order+1):] - u
        second_term_denominator = self.knot_vector[(order + 1):] - self.knot_vector[1:-order]

        # handle division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            first_term = np.where(first_term_denominator != 0.0, first_term_numerator / first_term_denominator, 0.0)
            second_term = np.where(second_term_denominator != 0.0, second_term_numerator / second_term_denominator, 0.0)
        
        
        return first_term[:-1] * previous_basis[:-1] + second_term * previous_basis[1:]
    
    def plot(self, n = 100):
        """
        Plots the spline curve over the whole knot vector with n uniformly spaced
        values
        """

        x_min = np.min(self.knot_vector)
        x_max = np.max(self.knot_vector)

        x_vals = np.linspace(x_min, x_max, num = n)
        y_vals = np.array([self(x) for x in x_vals]).T
        for basis_func in y_vals:
            plt.plot(x_vals, basis_func)
        plt.show()

class SplineCurve(object):
    """
    Inputs:
        knot_vector:
        control_points:
        order:
    Outputs:
        callable spline curve
    """
    def __init__(self, knot_vector, control_points, order=-1):
        
        """
        If order is not specified, it sets the maximum possible order
        with the given knot vector and control points
        """
        self.control_points = control_points
        self.knot_vector = knot_vector

        m = len(knot_vector)
        M = len(control_points)
        if order > m - M - 1 :
            print "exceeding max order %d" % order
            order = m - M - 1
            
        self.order = order
        self.basis = BSpline(knot_vector, order)
    def __call__(self, u):
        total = 0
        basis_funcs = self.basis(u)
        for i in range(len(self.control_points)):
            total += self.control_points[i] * basis_funcs[i]
        return total
    
    def plot(self, n = 30):
        x_min = np.min(self.knot_vector)
        x_max = np.max(self.knot_vector)

        x_vals = np.linspace(x_min, x_max, num = n)
        y_vals = np.array([self(x) for x in x_vals])

        plt.plot(x_vals, y_vals)
        plt.show()

if __name__ == "__main__":
    
    test = SplineCurve(knot_vector=[0, 0, 0, 1, 2, 3, 3, 3], control_points = [0, 0, 1, 0, 0],order=2)
    test.plot(n=100)
