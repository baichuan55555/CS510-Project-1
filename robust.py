import matplotlib.pyplot as plt
import numpy as np
import sympy
import cmath
import math


def _iterate_robust_step(func_list, func, deriv_func, xi, tol):
    fi = func(xi)
    der_yi = deriv_func(xi)

    # # failed
    # if abs(der_yi * fi) < tol:
    #     return None
    k = 1
    tmp_func = func_list[1]
    A = abs(fi)
    while abs(der_yi) < tol and k + 1 < len(func_list):
        k += 1
        tmp_func = func_list[k]
        der_yi = tmp_func(xi)

    uk = fi * der_yi.conjugate() / math.factorial(k)
    A = max(A, abs(der_yi) / math.factorial(k))
    j = k
    while j + 1 < len(func_list):
        j += 1
        tmp_func = func_list[j]
        der_yi = tmp_func(xi)
        A = max(A, abs(der_yi) / math.factorial(j))

    ukk = uk ** (k - 1)
    gamma = 2 * ukk.real
    delta = -2 * ukk.imag
    if abs(gamma) >= abs(delta):
        ck = abs(gamma)
        if gamma < 0:
            theta = 0
        else:
            theta = cmath.pi / k
    else:
        ck = abs(delta)
        if delta < 0:
            theta = cmath.pi / (2 * k)
        else:
            theta = 3 * cmath.pi / (2 * k)
    Ck = ck * (abs(uk) ** (2 - k)) / (6 * A * A)
    xj = xi + Ck * uk * cmath.exp(complex(0, 1) * theta) / abs(uk) / 3.0
    return xj


def _iterate_robust(func_list, func, deriv_func, x0, max_iter, tol):
    """
    Iteration process of robust newton's method

    Parameters
    ----------
    func: function
        the function
    deriv_func: function
        the derivative of the function
    """

    xi = x0
    xj = xi
    if abs(deriv_func(xj)) < tol:
        print(xj, '1')
        if abs(func(xj) * deriv_func(xj)) < tol:
            print(xj, '2')
    # print(func(xj) * deriv_func(xj), tol)
    for i in range(1, max_iter + 1):
        if abs(func(xj) * deriv_func(xj)) < tol:
            return i, xj
        xj = _iterate_robust_step(func_list, func, deriv_func, xi, tol)
        # print(xj)

        # close enough
        # if cmath.isclose(xi, xj, rel_tol=0, abs_tol=tol):
        #     return i, xj

        xi = xj
    xi = -100
    return i, xi


def robust_color_map(function, interval, num, max_iter=500, tol=1e-03, decimals=3):
    """
    Compute the color map of robust newton's method

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
    x = sympy.Symbol('x')
    func = eval("lambda x: " + function)
    deriv_func = eval("lambda x: " + str(sympy.diff(function, x)))
    func_list = [eval("lambda x: " + str(function))]
    while function:
        function = sympy.diff(function, x)
        func_list.append(eval("lambda x: " + str(function)))

    root_count = 0
    roots = {}
    color_map = np.zeros((num[0], num[1]))


    # for i, r in enumerate(np.linspace(interval[0], interval[1], num[0])):
        # for j, c in enumerate(np.linspace(interval[2], interval[3], num[1])):
    resolution = (interval[1] - interval[0]) / num[0]
    r = interval[0]
    for i in range(num[0]):
        c = interval[2]
        for j in range(num[0]):
            x0 = np.round(r + c*1j, decimals)
            # print(x0)
            # if abs(x0 - 0.8164) < tol:
            #     print(x0)
            root = np.round(_iterate_robust(func_list, func, deriv_func, x0, max_iter, tol)[1], decimals)
            if not root in roots:
                roots[root] = root_count
                root_count += 1
            color_map[i, j] = roots[root]
            c += resolution
        r += resolution
        print(i)
    # x0 = 0.8164
    # root = np.round(_iterate_robust(func_list, func, deriv_func, x0, max_iter, tol)[1], decimals)
    roots[root] = root_count
    return tuple(roots), color_map


def test_robust_color_map():
    # user_input = "x**3 - 3*x"
    user_input = "x**3 - 2 * x + 2"
    # user_input = "x**4 - 2*x**3 +2*x-1"
    interval = (-2, 2, -2, 2)
    num = (4000, 4000)

    roots, color_map = robust_color_map(user_input, interval, num)
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
    test_robust_color_map()
