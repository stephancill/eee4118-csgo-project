import time

from stable_baselines3 import A2C
import gym
from gym import spaces
from gsi.server import GSIServer
import pymem
import mouse
import numpy as np

from telnet_client.csgo_telnet_client import CSGOTelnetClient

Y_ANG_ADDR_OFFSET = 0x4dc4aec
X_ANG_ADDR_OFFSET = Y_ANG_ADDR_OFFSET+4

class CSGOEnvironment(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, timescale=4, render_mode: str = None):
        assert render_mode is None or render_mode in self.metadata["render.modes"]
        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=np.array([-180, -90]), high=np.array([180, 90]), shape=(2,))

        self.timescale = timescale

        self.server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
        self.server.start_server()

        self.pm = pymem.Pymem("csgo.exe")
        self.client = pymem.process.module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll
        
        self.telnet_client = CSGOTelnetClient()
        self.telnet_client.connect()

        self.telnet_client.run("exec bot")
        self.telnet_client.run(f"host_timescale {timescale}")


    def _get_obs(self):
        x_angle = np.float32(round(self.pm.read_float(self.client+X_ANG_ADDR_OFFSET), 2) - self.initial_state[0])
        y_angle = np.float32(round(self.pm.read_float(self.client+Y_ANG_ADDR_OFFSET), 2) - self.initial_state[1])
        return np.array([x_angle, y_angle])

    def reset(self):
        mouse.release()
        time.sleep(2/self.timescale) # There is a cooldown for the kill command
        self.telnet_client.run("kill")
        time.sleep(4/self.timescale)

        mouse.hold()
        self.initial_state = np.zeros((2,), dtype=np.float32)
        observation = self._get_obs()
        self.initial_state = observation
        return observation

    def step(self, action):
        ak_47 = [weapon for weapon in self.server.gamestate.player.weapons.values() if weapon["name"] == "weapon_ak47"][0]
        ammo = ak_47["ammo_clip"]
        reloading = ak_47["state"] == "reloading"
        mouse.move(action[0]*10, action[1]*10, absolute=False)
        done = ammo == 0
        observation = self._get_obs()
        sq = observation[0] ** 2 + observation[1] ** 2

        if sq < 500:
            if sq < 1:
                reward = 100/max(sq, 0.01)
            else:
                reward = -sq * 5
            reward += 100/max(30-ammo, 0.01)
        else:
            reward = -200000
            done = True

        print(reward)

        return observation, reward, done, {}
    
    def close(self):
        mouse.release()

    def render(self, mode=""):
        pass

if __name__ == "__main__":
    env = CSGOEnvironment(timescale=1)
    model = A2C()
