from gym.envs.registration import register
from .csgo_environment import CSGOEnvironment

register(
    id='CSGOEnvironment-v0',
    entry_point='custom_gym:CSGOEnvironment',
    max_episode_steps=300,
)