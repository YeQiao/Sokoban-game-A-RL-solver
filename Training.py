import gym
import griddly
import numpy as np
import gym_sokoban
import random
import time

env_name = 'Sokoban-small-v0'
env = gym.make(env_name)
ACTION_LOOKUP = env.unwrapped.get_action_lookup()
print("Created environment: {}".format(env_name))
q_table = np.zeros([7000,9])
# paramethers
alpha = 0.1
gamma = 0.7
epsilon = 0.15
episode = 2000
ACTION_LOOKUP = env.unwrapped.get_action_lookup()
count = 0
for i in range(1, episode):
    state = env.reset()
    # print(state)
    # break
    # epochs, reward = 0, 0
    done = False
    count += 1
    print("No. of episode",count)
    while not done:
        #if count > 900:
        #env.render(mode='human')
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()  # Explore action space
        else:
            action = np.argmax(q_table[state])
            #action = q_table[state].index(q_val)

        next_state, reward, done, info = env.step(action)

        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        state = next_state

np.savetxt("Array.txt", q_table, fmt="%s")
print("Training finished.")
