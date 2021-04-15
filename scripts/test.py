import sys
import gym
import numpy as np
from Agent import Agent

args = sys.argv
env_name = sys.argv[1]
num_testing_episodes = int(sys.argv[2])
num_policies = int(sys.argv[3])
policies = []
for i in range(num_policies):
	policy_name = sys.argv[4 + i]
	policy = np.load('policies/'+ policy_name,allow_pickle='TRUE').item()
	policies.append(policy)

env = gym.make(env_name)

agent = Agent()
for policy in policies:
	agent.test(env, num_testing_episodes, policy)