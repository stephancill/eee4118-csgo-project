import mouse 
import time
import keyboard

on_off_switch = False

if __name__ == "__main__":
    keyboard.add_hotkey('/', )
    time.sleep(1)
    i = 0
    while(True):
        time.sleep(0.01)
        if (on_off_switch):
            i += 1
            mouse.move(-50,0, absolute=False, duration=0.1)
            mouse.move(0,-50, absolute=False, duration=0.1)
            mouse.move(50,0, absolute=False, duration=0.1)
            mouse.move(0,50, absolute=False, duration=0.1)
            print("complete", i)
