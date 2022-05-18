from custom_gym import CSGOEnvironment
from stable_baselines3 import A2C, DQN
from stable_baselines3.common.evaluation import evaluate_policy
import os
import time

MODELS_DIRECTORY = "models"

if not os.path.exists(MODELS_DIRECTORY):
    os.makedirs(MODELS_DIRECTORY)

env = CSGOEnvironment( render_mode="human")
# Train the agent
model = A2C('MlpPolicy', env, verbose=1, learning_rate=0.01)
model.learn(total_timesteps=40_000)
t = time.time()
model.save(f"{MODELS_DIRECTORY}/ak47_{str(round(t))}")

# model = A2C.load(f"{MODELS_DIRECTORY}/ak47_1652834378")
obs = env.reset()
done = False
step = 0
while not done:
    action, _ = model.predict(obs, deterministic=True)
    print("Step {}".format(step + 1))
    print("Action: ", action)
    obs, reward, done, info = env.step(action)
    print('obs=', obs, 'reward=', reward, 'done=', done)
    if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        print("Goal reached!", "reward=", reward)
        break