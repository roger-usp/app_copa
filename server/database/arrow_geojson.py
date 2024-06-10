from sympy import solve, Eq, Symbol
import numpy as np 
import matplotlib.pyplot as plt

def get_u(ABx, ABy, theta):
    AB_module = (ABx**2 + ABy**2)**0.5
    ux = Symbol("ux")
    uy = Symbol("uy")
    eq1 = Eq(uy + (ABx/ABy)*ux, 0)
    eq2 = Eq((ux**2 + uy**2)**0.5, theta*AB_module/2)
    return solve([eq1, eq2], [ux,uy])


def get_arrow_points(A,B, theta=0.1):
    A,B = np.array(A), np.array(B)
    AB = B-A
    C = A + (1-theta)*AB
    
    u0, u1 = get_u(AB[0], AB[1], theta)
    u0, u1 = np.array(u0), np.array(u1)
    D = C+u0
    E = C+u1
    
    arrow_points = [A,B,D,B,E]
    arrow_points = [list(p) for p in arrow_points]
    return arrow_points
