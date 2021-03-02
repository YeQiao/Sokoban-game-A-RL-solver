import gym
import griddly
import numpy as np
import gym_sokoban
import random
import time

env_name = 'Sokoban-small-v0'
env = gym.make(env_name)
count = 0
total_epochs, total_penalties = 0, 0
episodes = 1000
for _ in range(episodes):
    state = env.reset()
    epochs, penalties, reward = 0, 0, 0
    done = False
    count += 1
    print("No. of episode",count)

    while not done:
        #env.render(mode='human')
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)

        if reward == -1:
            penalties += 1

        epochs += 1

    total_penalties += penalties
    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")