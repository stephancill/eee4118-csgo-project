from custom_gym import CSGOEnvironment
from stable_baselines3 import A2C, DDPG, DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
import os
import time

MODELS_DIRECTORY = "models"
TENSORBOARD_LOG = "tensorboard-logs"

if not os.path.exists(MODELS_DIRECTORY):
    os.makedirs(MODELS_DIRECTORY)

if not os.path.exists(TENSORBOARD_LOG):
    os.makedirs(TENSORBOARD_LOG)

env = CSGOEnvironment(render_mode="human", timescale=2)
wrapped_env = Monitor(env)
# Train the agent
model = A2C('MlpPolicy', wrapped_env, verbose=1, learning_rate=0.001, tensorboard_log=TENSORBOARD_LOG)

# TODO EvalCallback with same environment
model.learn(total_timesteps=4_000, log_interval=30)
t = time.time()
model.save(f"{MODELS_DIRECTORY}/ak47_{str(round(t))}")

# model = A2C.load(f"{MODELS_DIRECTORY}/ak47_1652911551")
obs = env.reset()
done = False
step = 0
while not done:
    action, _ = model.predict(obs, deterministic=True)
    step += 1
    print(step, action[0], action[1], sep=",")
    obs, reward, done, info = env.step(action)
    if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        print("Goal reached!", "reward=", reward)
        break