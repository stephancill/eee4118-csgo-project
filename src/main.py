from ast import dump
import pymem
import pymem.process
import hazedumper as offsets
import time

def main():
    pm = pymem.Pymem("csgo.exe")
    # client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    
    while True:
        time.sleep(0.1)
        y_angle = pm.read_float(0x0523A1F4) # TODO Use offset names to derive this
        x_angle = pm.read_float(0x0523A1F8)
        print(y_angle, x_angle)


if __name__ == '__main__':
    main()