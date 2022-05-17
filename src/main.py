from ast import dump
import pymem
import pymem.process
import time
from gsi import GSIServer
from collections import namedtuple
import mouse
import keyboard
import os

Y_ANG_ADDR_OFFSET = 0x4dc4aec # 0x05180684
X_ANG_ADDR_OFFSET = Y_ANG_ADDR_OFFSET+4
RECORDING_DIRECTORY = "recordings"

Sample = namedtuple("Sample", ["x", "y", "clip", "time"])
samples = []

should_record = False

def toggle():
    global should_record
    should_record = not should_record
    print("toggle recording", should_record)

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
        return bool(self.start_time) and self.start_time > 0

def normalise(data):
    ref = data[0]
    norm = [(ref - x) for x in data] # TODO: Properly normalise
    return norm

def mse(samples):
    x_err_sq = sum([n_x**2 for n_x in normalise([s.x for s in samples])])
    y_err_sq = sum([n_y**2 for n_y in normalise([s.y for s in samples])])
    return (x_err_sq + y_err_sq) / (len(samples)) # TODO: Idk if this is right

def main():
    server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    server.start_server()

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    
    ammo = 0
    y_angle = 0
    x_angle = 0

    recorder = Recorder()

    keyboard.add_hotkey('/', toggle)
    
    def mouse_hook_callback(event):
        try:
            if event.event_type == "down" and event.button == "left" and not recorder.is_recording and should_record:
                recorder.start()
            elif event.event_type == "up" and event.button == "left" and recorder.is_recording:
                recorder.end()
        except:
            pass

    mouse.hook(mouse_hook_callback)

    while True:
        ammo = server.gamestate.player.weapons["weapon_2"]["ammo_clip"]
        y_angle = round(pm.read_float(client+Y_ANG_ADDR_OFFSET), 2)
        x_angle = round(pm.read_float(client+X_ANG_ADDR_OFFSET), 2)

        if recorder.is_recording:
            recorder.sample(x_angle, y_angle, ammo)

        if ammo == 0 and recorder.is_recording:
            recorder.end()
            mouse.release()
            # TODO: Evaluate performance
            print("error", mse(recorder.samples))
            time.sleep(3)

        elif ammo == 30 and not recorder.is_recording and should_record:
            mouse.hold()
            

        # print(x_angle, y_angle)

        time.sleep(0.01)


if __name__ == '__main__':
    main()