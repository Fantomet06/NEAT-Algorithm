import gym

env = gym.make('CartPole-v1')

observation = env.reset()

print(observation)
print(env.action_space)

done = False
while not done:
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(observation, reward, done, info)
    env.render()