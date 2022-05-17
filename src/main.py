import re
import pymem
import pymem.process
import time
from gsi import GSIServer
from recorder import Recorder
import mouse
import keyboard
from telnet_client import CSGOTelnetClient


Y_ANG_ADDR_OFFSET = 0x4dc4aec # 0x05180684
X_ANG_ADDR_OFFSET = Y_ANG_ADDR_OFFSET+4


samples = []

should_record = False

def toggle():
    global should_record
    should_record = not should_record
    print("toggle recording", should_record)



def normalise(data):
    ref = data[0]
    norm = [(ref - x) for x in data] # TODO: Properly normalise
    return norm

def mse(samples):
    x_err_sq = sum([n_x**2 for n_x in normalise([s.x for s in samples])])
    y_err_sq = sum([n_y**2 for n_y in normalise([s.y for s in samples])])
    return (x_err_sq + y_err_sq) / (len(samples)) # TODO: Idk if this is right

def act(time):
    print("taking action for time", time)
    mouse.move(-1, 1, absolute=False)

def reset(telnet_client: CSGOTelnetClient):
    time.sleep(0.5) # There is a cooldown for the kill command
    telnet_client.run("kill")
    time.sleep(1)

def main():
    server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    server.start_server()

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    
    ammo = 0
    y_angle = 0
    x_angle = 0
    reloading = False

    recorder = Recorder()
    telnet_client = CSGOTelnetClient()
    telnet_client.connect()

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
        ak_47 = [weapon for weapon in server.gamestate.player.weapons.values() if weapon["name"] == "weapon_ak47"][0]
        ammo = ak_47["ammo_clip"]
        reloading = ak_47["state"] == "reloading"
        
        if recorder.is_recording:
            y_angle = round(pm.read_float(client+Y_ANG_ADDR_OFFSET), 2)
            x_angle = round(pm.read_float(client+X_ANG_ADDR_OFFSET), 2)
            recorder.sample(x_angle, y_angle, ammo)
            # TODO: Get action and execute
            act(recorder.relative_time)

        if ammo == 0 and not reloading and recorder.is_recording:
            recorder.end()
            mouse.release()
            # TODO: Evaluate performance
            print("error", mse(recorder.samples))
            
        elif reloading and not recorder.is_recording and should_record:
            reset(telnet_client)
            mouse.hold()


        # print(x_angle, y_angle)

        time.sleep(0.01)


if __name__ == '__main__':
    main()