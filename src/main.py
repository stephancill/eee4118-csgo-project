from ast import dump
import pymem
import pymem.process
import hazedumper as offsets
import time
from gsi import GSIServer

ANG_ADDR = 0x9FD2808

def main():
    server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    server.start_server()
    print("done")

    pm = pymem.Pymem("csgo.exe")
    # client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    print(server.gamestate.player.weapons)

    ammo = 0
    y_angle = 0
    x_angle = 0

    while True:
        time.sleep(0.01)
        ammo_new = server.gamestate.player.weapons["weapon_2"]["ammo_clip"]
        y_angle_new = round(pm.read_float(ANG_ADDR), 2)
        x_angle_new = round(pm.read_float(ANG_ADDR+4), 2)

        if ammo_new != ammo or y_angle_new != y_angle or x_angle_new != x_angle: 
            ammo = ammo_new
            y_angle = y_angle_new
            x_angle = x_angle_new
            print(round(y_angle, 2), round(x_angle, 2), ammo)


if __name__ == '__main__':
    main()