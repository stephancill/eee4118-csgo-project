
import os
from collections import namedtuple
import time

RECORDING_DIRECTORY = "recordings"
Sample = namedtuple("Sample", ["x", "y", "clip", "time"])

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
    def relative_time(self):
        return time.time() - self.start_time

    @property
    def is_recording(self):
        return bool(self.start_time) and self.start_time > 0