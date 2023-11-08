import numpy as np
import matplotlib.pyplot as plt
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

def cubic_bezier(p0, a, b, p1):
    return lambda t: np.power(1-t,3)*p0 + 3*t*np.power(1-t,2)*a + 3*(1-t)*np.power(t,2)*b + np.power(t,3)*p1

def bezier(P, step):
    A, B = bezier_interpolate(P)
    gamma = [ cubic_bezier(P[i], A[i], B[i], P[i + 1])
              for i in range(len(P) - 1) ]
    print(gamma)
    bezier = np.array([g(t) for g in gamma for t in np.linspace(0,1,step)])
    return bezier, A, B