import numpy as np
from cfd_aero_sim import airfoil_from_naca4
import cma
from cma import CMAEvolutionStrategy
import matplotlib.pyplot as plt

m=2*0.01
p=4*0.01
t=12*0.01
c=1.0

params = [m, p, t, c]
def compute_cl_cd_ratio(params: list):
    airfoil = airfoil_from_naca4(params)
    # return airfoil["CL"][0]/airfoil["CD"][0]
    return airfoil["CL"]/airfoil["CD"]

es = CMAEvolutionStrategy(x0=params[:-1], sigma0=0.5)
es.opts.set({"tolfacupx": 1e5})
es.opts.set({"tolx": 1e-4})
es.opts.set({"tolstagnation": 1000})

best_vals = []

while not es.stop():
    solutions = es.ask()
    fitnesses = [compute_cl_cd_ratio(np.append(x, params[-1])).item() for x in solutions]
    es.tell(solutions, fitnesses)
    es.logger.add()
    best_vals.append(max(fitnesses))
    es.disp()

es.result_pretty()
try:
    # es.logger.plot()
    plt.plot(best_vals)
    plt.xlabel("Iteration")
    plt.ylabel("Best CL/CD")
    plt.title("Best Lift to Drag Ratio from CMAES")
    plt.savefig("./lacsef_stats/CMAES_Optimization_New", dpi=200, bbox_inches="tight")
    plt.show()
except Exception as e:
    print(f"Error\n{e}")
# cma.s.figsave("./lacsef_stats/CMAES_Optimization")
