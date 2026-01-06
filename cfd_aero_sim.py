import numpy as np
import neuralfoil as nf
import matplotlib.pyplot as plt
import aerosandbox as asb
from airfoil_parameter import airfoil_from_naca4_params

def airfoil_coords_from_naca4(m:float, p:float, t:float, c:float, n:int=100) -> np.array:
    xu, yu, xl, yl, x, yc = airfoil_from_naca4_params([m, p, t, c])
    x_upper = xu
    y_upper = yu
    x_lower = xl
    y_lower = yl

    total_x = np.concatenate([x_upper, x_lower])
    total_y = np.concatenate([y_upper, y_lower])

    # normalization
    total_x = total_x - np.min(total_x)
    chord = np.max(total_x)
    total_x = total_x / chord
    total_y = total_y / chord
    # return np.column_stack((total_x, total_y))
    return [total_x, total_y]

def airfoil_from_naca4(params:list):
    x, y = airfoil_coords_from_naca4(params[0], params[1], params[2], params[3])
    airfoil = nf.get_aero_from_coordinates(
        coordinates=np.column_stack([x, y]),
        alpha=5.0,
        Re=5e6
    )

    return airfoil

m=2*0.01
p=4*0.01
t=12*0.01
c=1.0
# naca4_params = [0.01*m, 0.1*p, 0.01*t, c]

try:
    x, y = airfoil_coords_from_naca4(m=m, p=p, t=t, c=c)
    test = np.column_stack([x, y])
    # print(f"DIM_TEST: {test.ndim}")
except Exception as e:
    print(f"ERROR\n {e}")

# print(f"Min X: {np.min(x)}\nMin Y: {np.min(y)}\nMax X: {np.max(x)}\nMax Y: {np.max(y)}")
plt.plot(x, y)
plt.axis("equal")
# plt.savefig("./lacsef_stats/NACA4_Debugging_Parameterization_CFD_NeuralFoil")
# plt.show()

airfoil = nf.get_aero_from_coordinates(
    coordinates=test,
    alpha=5.0,
    Re=5e6
)
# print(f"Coefficient for Lift: {airfoil["CL"]}\nCoefficient for Drag: {airfoil["CD"]}\nConfidence: {airfoil["analysis_confidence"]}\nCM: {airfoil["CM"]}")

if __name__ == "__main__":
    x, y = airfoil_coords_from_naca4(m, p, t, c)

"""
with open("./lacsef_stats/fixed_parameterization_error.txt", "w") as f:
    for key, val in airfoil.items():
        f.write(f"{key}: {val}\n")

# xu, yu, xl, yl, x, yc = airfoil_from_naca4_params(naca4_params)
test_x = np.concatenate([xu, xl])
print(f"X dim: {test_x.ndim}, Shape: {test_x.shape}")
test_y = np.concatenate([yu, yl])
print(f"Y dim: {test_y.ndim}, Shape: {test_y.shape}")

test = np.column_stack((test_x, test_y))
print(f"NDIMS: {test.ndim} \n{test.shape}")

nf.get_aero_from_coordinates(
    coordinates=test, # needs to be (100,2) np array
    alpha=5.0,
    Re=5e6,
)
"""