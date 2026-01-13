import gymnasium as gym
from gymnasium.utils.env_checker import check_env

env = gym.make("cfd-v0")
try:
    check_env(env)
    print("Envrionment works")
except Exception as e:
    print(f"Envrionment has issues:\n{e}")