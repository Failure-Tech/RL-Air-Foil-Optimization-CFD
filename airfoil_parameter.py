import matplotlib.pyplot as plt
import numpy as np
import math as mt

# Parametric Generator Function
# params => [max_camber, camber_pos, max_thickness, thick_pos, LE_radius, TE_angle]
def airfoil_symmetric_from_params(params: list, n_points:int=100) -> list:
    x = np.linspace(0, 1, n_points)
    camber_line = (params[2])/(np.square(params[3])) * (2*params[3]*x - np.square(x))

    y_t = params[2] * (0.2969 * np.sqrt(x) - 0.1260*x - 0.3516 * np.square(x) + 0.2843 * np.pow(x, 3) - 0.1015 * np.pow(x, 4))

    y_upper = camber_line - y_t
    y_lower = y_t + camber_line

    """
    with open("test.dat", "w") as f:
        f.write("Test\n")
        f.write(str(x).removeprefix("[").removesuffix("]"))
    """

    return [x, y_lower, y_upper]

def airfoil_from_naca4_params(params: list, n_points:int=100) -> list:
    # input params
    """[max camber, max camber pos, thickness, chord len] => [m, p, t, c]"""
    # coeffs for 4 digit airfoil series
    a0=1.4845
    a1=-0.6300
    a2=-1.7580
    a3=1.4215
    a4=-0.5075

    coeffs = [a0, a1, a2, a3, a4]

    x = np.linspace(0, params[-1], n_points)
    y = np.zeros(n_points)
    yc = np.zeros(n_points)
    dyc = np.zeros(n_points)
    yt = np.zeros(n_points)
    xu = np.zeros(n_points)
    yu = np.zeros(n_points)
    xl = np.zeros(n_points)
    yl = np.zeros(n_points)
    # [m, p, t, c]
    for i in range(n_points):
        if (x[i]/params[-1] < params[1]):
            yc[i] = (params[-1]*params[0]/(params[1]**2))*(2*params[1]*(x[i]/params[-1]) - (x[i]/params[-1])**2)
            dyc[i] = ((params[0]*2)/params[1]**2) * (params[1] - (x[i]/params[-1]))
        else:
            yc[i] = (params[-1]*params[0]/(1-params[1])**2) * (1-2*params[1] + 2*params[1]*(x[i]/params[-1]) - (x[i]/params[-1])**2)
            dyc[i] = ((2*params[0])/(1-params[1])**2) * (params[1] - (x[i]/params[-1]))

    for i in range(n_points):
        yt[i] = params[2]*params[-1] * (coeffs[0] * mt.sqrt(x[i]/params[-1]) + coeffs[1]*(x[i]/params[-1]) + coeffs[2]*(x[i]/params[-1])**2 + coeffs[3]*(x[i]/params[-1])**3 + coeffs[4]*(x[i]/params[-1])**4)
        theta = mt.atan(dyc[i])
        xu[i] = x[i] - yt[i]*mt.sin(theta)
        xl[i] = x[i] + yt[i]*mt.sin(theta)
        yu[i] = yc[i] + yt[i]*mt.cos(theta)
        yl[i] = yc[i] - yt[i]*mt.cos(theta)

    return [xu, yu, xl, yl, x, yc]

# ex: naca 0012 basic params
naca_0012_params = np.array([0.0, 0.4, 0.12, 0.4, 0.005, 0.0])
# airfoil_symmetric_from_params(naca_0012_params)
# airfoil = airfoil_from_params(naca_0012_params)
# print(list(airfoil[1]))

m=2
p=4
t=12
c=2
naca4_params = [0.01*m, 0.1*p, 0.01*t, c]
airfoil = airfoil_from_naca4_params(naca4_params)
# print(airfoil[0][1])

# plt.xlim(-0.2, naca4_params[-1]+0.2)
# plt.ylim(-naca4_params[-1]/3, naca4_params[-1]/3)
# plt.plot(airfoil[0], airfoil[1], color="red")
# plt.plot(airfoil[2], airfoil[3], color="deepskyblue")
# plt.plot(airfoil[4], airfoil[5], "g--")
# plt.yticks([])
# plt.xticks([])
# plt.savefig("./lacsef_stats/NACA_4_Parameterization_and_Airfoil_Generation_Fixed")
# plt.show()
# plt.close()