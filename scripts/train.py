import sys
import gym
import numpy as np
from QLearningAgent import QLearningAgent

env = gym.make('FrozenLake8x8-v0')
num_training_episodes = 1000
num_testing_episodes = 100000

args = sys.argv
algo = sys.argv[1]
state_space_size = int(sys.argv[2])
action_space_size = int(sys.argv[3])

agent = None
if algo == 'q_learning':
	agent = QLearningAgent()
	agent.train(env, state_space_size, action_space_size, num_training_episodes)

# print(algo)
# print(state_space_size)
# print(action_space_size)