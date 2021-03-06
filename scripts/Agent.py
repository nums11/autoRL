import random
import numpy as np
from tqdm import tqdm
import collections
from collections import Counter
import matplotlib.pyplot as plt
import time

class Agent:
  def printRewards(self, split, num_episodes, rewards):
    rewards_per_split_episodes = np.split(np.array(rewards),num_episodes/split)
    count = split

    print(f"\n********Average reward per {split} episodes ********\n")
    for r in rewards_per_split_episodes:
      print(count, ": ", str(sum(r/split)))
      count += split

  def savePolicyFromQTable(self, q_table, algo_prefix, num_episodes):
    episode_str = ''
    if num_episodes >= 1000000:
      episode_str = str(int(num_episodes / 1000000)) + 'mil'
    elif num_episodes >= 1000:
      episode_str = str(int(num_episodes / 1000)) + 'k'
    else:
      episode_str = str(num_episodes)
    policy_name = algo_prefix + '_' + 'policy_' + episode_str
    policy = self.getPolicyFromQTable(q_table)
    np.save('policies/' + policy_name + '.npy', policy)

  def getPolicyFromQTable(self, q_table):
    policy = {}
    for i in range(len(q_table)):
      policy[i] = np.argmax(q_table[i])
    return policy

  def test(self, env, num_episodes, policy):
    done = False
    rewards_all_episodes = []

    print("Beginning Testing")
    for episode in range(num_episodes):
      print(f'Episode {episode} / {num_episodes}')
      state = env.reset()
      done = False
      rewards_current_episode = 0

      while True:
        if done:
          rewards_all_episodes.append(rewards_current_episode)
          break
        action = policy[state]
        new_state, reward, done, info = env.step(action)
        rewards_current_episode += reward
        state = new_state
    print('Done Testing')

    avg_rewards = sum(rewards_all_episodes) / num_episodes
    print(f'******* Average rewards across {num_episodes} episodes *******')
    print(avg_rewards)
    counts = Counter(rewards_all_episodes)
    win_rate = (counts[1] / len(rewards_all_episodes)) * 100
    print(f'{win_rate}% win rate')


  def testVisual(self, env, num_episodes, policy):
    for episode in range(num_episodes):
      print("*****EPISODE ", episode+1, "*****\n")
      time.sleep(1)

      state = env.reset()
      done = False
      while True:       
        env.render()
        time.sleep(0.1)
        action = policy[state]
        new_state, reward, done, info = env.step(action)
        state = new_state

        if done:
          env.render()
          if reward == 1:
            print("****You reached the goal!****\n")
            time.sleep(3)
          else:
            print("****You fell through a hole!****\n")
            time.sleep(3)
          break

    env.close()