import numpy as np
import matplotlib.pyplot as plt
import linear
from scipy.linalg import solveh_banded
import copy

def get_diagonals(n):
    return np.r_[[np.r_[[0], np.ones(n-2), [2]]],
                 [np.r_[[2], 4*np.ones(n-2), [7]]],
                 [np.r_[np.ones(n-1), [0]]]]

def thomas_solve(diagonals,d):
        a,b,c = copy.deepcopy(diagonals)
        n = len(b)
        
        for i in range(1,n):
            w = a[i] / b[i-1]
            b[i] -= w*c[i-1]
            d[i] -= w*d[i-1]

        x = np.zeros((n,2))
        x[n-1] = d[n-1] / b[n-1]
        for i in range(n-2,-1,-1):
            x[i] = (d[i] - c[i]*x[i+1]) / b[i]
        
        return x

def bezier_interpolate(points):
    n = len(points)-1

    P = np.array([points[0] + 2*points[1] if i == 0 
                  else 8*points[n-1]+points[n] if i == n-1
                  else 2*(2*points[i] + points[i + 1]) for i in range(n)])

    diagonals = get_diagonals(n)
    A = thomas_solve(diagonals, P)

    B = np.zeros((n,2))
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A,B

def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * \
        t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = bezier_interpolate(points)
    return [ get_cubic(points[i], A[i], B[i], points[i + 1])
             for i in range(len(points) - 1) ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    if len(points) < 3 : return
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])

def bezier(points, step):
    if len(points) < 3: return
    A, B = bezier_interpolate(points)
    curve_slices = get_bezier_cubic(points)
    curve = np.array([fun(t) for fun in curve_slices for t in np.linspace(0, 1, step)])
    return curve, A, B