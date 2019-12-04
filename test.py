import numpy as np
import sympy
import matplotlib.pyplot as plt
import cmath


def newton(function, x0, max_iter=500, tol=1e-08):
    """ 
    Newton's method
    Parameters
    ----------
    function: string
        The function that we want to find its root
    x0: complex number
        The start point, it looks like 5 + 5 * I
    tol: float  
        the max error we accept
    max_iter: int
        the max iteration we accept
    Returns
    -------
    int
        number of iteration
    complex number
        root of func
    """

    func = eval("lambda x: " + function)
    deriv_func = eval("lambda x: " + str(sympy.diff(function)))

    return _iterate_newton(func, deriv_func, x0, max_iter, tol)

def _iterate_newton(func, deriv_func, x0, max_iter=500, tol=1e-08):
    """
    Iteration process of newton's method
    Parameters
    ----------
    func: function
        the function
    deriv_func: function
        the derivative of the function
    """

    xi = x0
    for i in range(1, max_iter + 1):
        fi = func(xi)
        der_yi = deriv_func(xi)

        # failed
        if der_yi == 0:
            return i, None

        xj = xi - fi / der_yi

        # close enough
        if cmath.isclose(xi, xj, rel_tol=0, abs_tol=tol):
            return i, xj

        xi = xj

    return i, xi


def newton_color_map(function, interval, num, max_iter=500, tol=1e-08, decimals=4):
    """
    Compute the color map of newton's method
    Parameters
    ----------
    interval: tuple with size of 4
        define the range of real and complex parts
        (real_min, real_max, complex_min, complex_max)
    num: tuple with size of 2
        define the number of points
        (num_real, num_complex)
    Returns
    -------
    tuple
        all roots found in the interval
    2D numpy array
        class of a point
    """
    func = eval("lambda x: " + function)
    deriv_func = eval("lambda x: " + str(sympy.diff(function)))
    root_count = 0
    roots = {}
    color_map = np.zeros((num[0], num[1]))

    for i, r in enumerate(np.linspace(interval[0], interval[1], num[0])):
        for j, c in enumerate(np.linspace(interval[2], interval[3], num[1])):
            x0 = r + c*1j
            root = np.round(_iterate_newton(func, deriv_func, x0, max_iter, tol)[1], decimals)
            if not root in roots:
                roots[root] = root_count
                root_count += 1
            color_map[i, j] = roots[root]

    return tuple(roots), color_map

def test_newton():
    user_input = "x**3 - 1"
    x0 = 1 + 1j
    iteration, root = newton(user_input, x0)
    print("Iteration:", iteration)
    print("Converge to:", root)

    # for test purpose
    func = sympy.Poly(user_input)
    print('\nAll roots from sympy')
    roots = func.all_roots()
    print(roots)

def test_newton_color_map():
    user_input = "x**3 - 2*x + 2"
    interval = (-2, 2, -2, 2)
    num = (400, 400)

    roots, color_map = newton_color_map(user_input, interval, num)
    print(roots)
    
    # for test purpose
    func = sympy.Poly(user_input)
    print('\nAll roots from sympy')
    roots = func.all_roots()
    print(roots)

    # TODO: find a good cmap
    plt.imshow(color_map.T, cmap='brg', extent=interval)
    plt.show()

if __name__ == "__main__":
    # test_newton()

    test_newton_color_map()