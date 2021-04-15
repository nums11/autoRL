import sys
import gym
import numpy as np
from QLearningAgent import QLearningAgent
from MonteCarloAgent import MonteCarloAgent
from SarsaAgent import SarsaAgent
from DoubleQLearningAgent import DoubleQLearningAgent
from NStepSarsaAgent import NStepSarsaAgent
from ExpectedSarsaAgent import ExpectedSarsaAgent

args = sys.argv
env_name = sys.argv[1]
algo = sys.argv[2]
n = int(sys.argv[3])
learning_rate = float(sys.argv[4])
epsilon = float(sys.argv[5])
min_epsilon = float(sys.argv[6])
epsilon_decay_rate = float(sys.argv[7])
discount_factor = float(sys.argv[8])
max_steps_per_episode = int(sys.argv[9])
num_episode_sets = int(sys.argv[10])
episode_sets = []
for i in range(num_episode_sets):
	episode_sets.append(int(sys.argv[11 + i]))

env = gym.make(env_name)
state_space_size = env.observation_space.n
action_space_size = env.action_space.n

agent = None
if algo == 'q_learning':
	agent = QLearningAgent()
elif algo == 'monte_carlo':
	agent = MonteCarloAgent()
elif algo == 'sarsa':
	agent = SarsaAgent()
elif algo == 'expected_sarsa':
	agent = ExpectedSarsaAgent()
elif algo == 'double_q_learning':
	agent = DoubleQLearningAgent()
elif algo == 'n_step_sarsa':
	agent = NStepSarsaAgent()

for num_training_episodes in episode_sets:
	if algo == 'n_step_sarsa':
		agent.train(env, n, state_space_size, action_space_size, num_training_episodes,
			learning_rate, epsilon, min_epsilon, epsilon_decay_rate, discount_factor,
			max_steps_per_episode)
	elif algo == 'monte_carlo':
		agent.train(env, state_space_size, action_space_size, num_training_episodes,
			discount_factor)
	else:
		agent.train(env, state_space_size, action_space_size, num_training_episodes,
			learning_rate, epsilon, min_epsilon, epsilon_decay_rate, discount_factor,
			max_steps_per_episode)