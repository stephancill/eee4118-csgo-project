from turtle import onscreenclick
import mouse 
import time
import keyboard

on_off_switch = False

def toggle():
    global on_off_switch
    on_off_switch = not on_off_switch

if __name__ == "__main__":
    keyboard.add_hotkey('/', lambda: toggle())
    mouse.move(25,25, absolute=False, duration=1)
    time.sleep(1)

    while(True):
        if (on_off_switch):
            mouse.move(-50,0, absolute=False, duration=1)
            mouse.move(0,-50, absolute=False, duration=1)
            mouse.move(50,0, absolute=False, duration=1)
            mouse.move(0,50, absolute=False, duration=1)
            time.sleep(0.01)
