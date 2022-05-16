from turtle import onscreenclick
import mouse 
import time
import keyboard

on_off_switch = False

def toggle():
    print("toggle")
    global on_off_switch
    on_off_switch = not on_off_switch

if __name__ == "__main__":
    keyboard.add_hotkey('/', toggle)
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
