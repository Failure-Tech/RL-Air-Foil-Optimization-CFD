import gymnasium as gym
import numpy as np
from typing import Optional
from cfd_aero_sim import airfoil_from_naca4

class Env(gym.Env):
    def __init__(self):
        super().__init__()
        self.c: np.float64 = 1.0

        self._params = np.array(0, dtype=np.float64)*4
        
        self.action_space = gym.spaces.Tuple(
            gym.spaces.Discrete(3),
            gym.spaces.Box(0.0, 1.0, (3,), dtype=np.float64)
        )

        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(3,)
        )

        self._action_to_step = {
            1: np.array(np.random.uniform(0, 1, step=1)),
            2: np.array(np.random.uniform(0, 1, step=2)),
            3: np.array(np.random.uniform(0, 1, step=3)),
        }

    def _get_obs(self):
        return {
            "params": self._params
        }

    def _get_info(self):
        return {
            "action": self._action_to_step
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed)

        self._params = np.append(np.zeros(np.float64)*3, self.c)

        observation = self._get_obs()
        info = self._get_info()

        return tuple(observation, info)
    
    def step(self, action):
        """
        args:
            action: decides between 1, 2, or 3 variables to change for generating airfoil
            
            figure out how to sample variables + generate between 0-1
        """

        action_step = action+1
        airfoil = airfoil_from_naca4(np.append(self._action_to_step[action], self.c))

        terminated = airfoil["analysis_confidence"].item() > 0.95

        truncated = False

        # change reward function to match airfoil [cl, cd, cl/cd, analy, cm]
        reward = 1 if terminated else ((-0.2*airfoil["CL"]/airfoil["CD"]).item() -0.2*airfoil["CL"].item() 0.2*+ airfoil["CD"].item -0.2*airfoil["analysis_confidence"].item() + 0.2*airfoil["CM"].item())

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info