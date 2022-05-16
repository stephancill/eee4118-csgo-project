from ast import dump
import pymem
import pymem.process
import time
from gsi import GSIServer
from collections import namedtuple
import mouse
import os

Y_ANG_ADDR = 0x0545077C
X_ANG_ADDR = 0x7141A940
RECORDING_DIRECTORY = "recordings"

Sample = namedtuple("Sample", ["x", "y", "clip", "time"])
samples = []

class Recorder:
    def __init__(self):
        self.samples = None
        self.start_time = None
    
    def start(self):
        if not os.path.exists(RECORDING_DIRECTORY):
            os.makedirs(RECORDING_DIRECTORY)
        self.start_time = time.time()
        self.samples = []
        print("started", self.start_time, bool(self.start_time))
    
    def sample(self, x, y, clip):
        self.samples.append(Sample(x, y, clip, time.time() - self.start_time))

    def end(self, write=False):
        print("ended", self.start_time)
        print("ended", len(self.samples), "samples", time.time() - self.start_time, "seconds")
        if write:
            with open(f"{RECORDING_DIRECTORY}/spray_{str(round(self.start_time))}.csv", "w") as f:
                f.write("x,y,clip,time\n")
                for sample in self.samples:
                    f.write(",".join([str(x) for x in [sample.x, sample.y, sample.clip, sample.time]]) + "\n")
        self.start_time = None

    @property
    def is_recording(self):
        return self.start_time and self.start_time > 0



def main():
    server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    server.start_server()
    print("done")

    pm = pymem.Pymem("csgo.exe")

    ammo = 0
    y_angle = 0
    x_angle = 0

    recorder = Recorder()

    

    def mouse_hook_callback(event):
        try:
            if event.event_type == "down" and event.button == "left" and not recorder.is_recording:
                recorder.start()
            elif event.event_type == "up" and event.button == "left" and recorder.is_recording:
                recorder.end()
        except:
            pass

    mouse.hook(mouse_hook_callback)

    while True:
        ammo = server.gamestate.player.weapons["weapon_2"]["ammo_clip"]
        y_angle = round(pm.read_float(Y_ANG_ADDR), 2)
        x_angle = round(pm.read_float(X_ANG_ADDR), 2)

        if recorder.is_recording:
            recorder.sample(x_angle, y_angle, ammo)

        if ammo == 0 and recorder.is_recording:
            recorder.end(write=True)
            # TODO: Mouse up, mouse down
        
        # print(x_angle, y_angle)

        time.sleep(0.01)


if __name__ == '__main__':
    main()