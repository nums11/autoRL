from Agent import *

class NStepSarsaAgent(Agent):
  def train(self, env, n, state_space_size, action_space_size, num_episodes,
    learning_rate, epsilon, min_epsilon, epsilon_decay_rate, discount_factor,
    max_steps_per_episode):
    rewards_all_episodes = []
    q_table = np.zeros((state_space_size, action_space_size))
    farthest_states = {}

    print('Beginning Training')
    for episode in range(num_episodes):
      print(f'Episode {episode} / {num_episodes}')
      state = env.reset()
      rewards_current_episode = 0
      farthest_state_for_episode = 0
      t = 0
      T = np.inf

      action = None
      exploration_rate_threshold = random.uniform(0, 1)
      if exploration_rate_threshold > epsilon:
        action = np.argmax(q_table[state]) 
      else:
        action = random.randint(0,3)

      actions = [action]
      states = [0]
      rewards = [0]

      for step in range(max_steps_per_episode):
        if t < T:
          if state > farthest_state_for_episode:
            farthest_state_for_episode = state

          new_state, reward, done, info = env.step(action)
          states.append(new_state)
          rewards.append(reward)

          if done:
            T = t + 1
            if reward > 0:
              print("I won!", reward)
          else:
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > epsilon:
              action = np.argmax(q_table[state]) 
            else:
              action = random.randint(0,3)
            actions.append(action)

        tau = t - n + 1
        if tau >= 0:
          G = 0
          for i in range(tau + 1, min(tau+n+1, T+1)):
            G += np.power(discount_factor, i - tau - 1) * rewards[i]
          if (tau + n) < T:
            G += np.power(discount_factor, n) * q_table[states[tau+n]][actions[tau+n]]
          q_table[states[tau],actions[tau]] = q_table[states[tau]][actions[tau]] + \
            learning_rate * (G - q_table[states[tau]][actions[tau]])

        state = new_state
        rewards_current_episode += reward

        if tau == T - 1:
          break

        t += 1

      # Exponentially decay epsilon
      epsilon = min_epsilon + \
        (1 - min_epsilon) * np.exp(-epsilon_decay_rate*episode)
      rewards_all_episodes.append(rewards_current_episode)

      if farthest_state_for_episode in farthest_states:
        farthest_states[farthest_state_for_episode] += 1
      else:
        farthest_states[farthest_state_for_episode] = 0

    print('Done Training')

    self.printRewards(num_episodes/10, num_episodes, rewards_all_episodes)
    print("q_table", q_table)
    self.savePolicyFromQTable(q_table, str(n) + '_step_sarsa', num_episodes)
    # farthest_states_ordered = collections.OrderedDict(sorted(farthest_states.items()))
    # self.plotFarthestStates(farthest_states_ordered)

  def plotFarthestStates(self, farthest_states_ordered):
    print("farthest_states_ordered", farthest_states_ordered)
    states = list(farthest_states_ordered.keys())
    frequencies = list(farthest_states_ordered.values())
    plt.bar(states,frequencies, width = 0.4)
    plt.xlabel("States")
    plt.ylabel("Frequencies")
    plt.title("Frequency of farthest states")
    plt.show()



