"""
State: current airfoil metrics [CL, CD, CL/CD, CM, analysis_confidence]
Action: generate new naca4 parameters to generate airfoil
Reward: use airfoil metrics

Skill: generate good naca4 parameters for airfoil
Information: current airfoil + airfoil metrics
Actions: generate 3 floats [m, p, t], with c=1 appended each time
Success: when metrics are optimal
End: time limit
"""

import gymnasium as gym
from typing import Optional
import numpy as np

class AirfoilGym(gym.Env):
    def __init__(self, airfoil: Optional[any]):
        # super.__init__(AirfoilGym, self)
        # intialize states [m, p, t, c]
        self._agent_params = np.array(-0.1)*4
        self._airfoil = None

        # treating obs_space as state_space => 3 random floats + 1.0 for c at the end
        self.observation_space = gym.spaces.Dict(
            {
                "agent_params": np.append(gym.spaces.Box(0, 1, shape=(3,), dtype=np.float64), 1.0),
                "airfoil": airfoil if not None else None
            }
        )
        # generate 3 float values in continuous action space
        self.action_space = gym.spaces.Box(0, 1, shape=(3,), dtype=np.float64)

    def _get_obs(self):
        return {
            "agent_params": self._agent_params,
            "airfoil": self._airfoil
        }

    def _get_info(self):
        "returning a dictionary "
        pass

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)

        # randomly generate 3 numbers
        self._agent_params = np.append(self.np_random.float64(0, 3, size=3, dtype=np.float64), 1.0)

        observation = self._get_obs()
        # info = self._get_info()

        return observation

    def step(self, action):
        """
        One timestep in this enviroinment
        Args:
        action: the continuous action that generates the three variables

        returns (observation, reward, terminated, truncated)
        """
        params: list = [np.random.uniform(0, 1)]

        terminated = True

        truncated = False

        observation = self._get_obs()
        info = self._get_info()

        # change function
        reward = 1 if terminated else 0

        return observation, reward, terminated, truncated, info