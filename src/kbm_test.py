# import mouse 
from asyncio.windows_events import NULL
from contextlib import nullcontext
import pyautogui
import time
import keyboard
import mouse

on_off_switch = False
SAMPLERATE = 0.05

def toggle():
    print("toggle")
    global on_off_switch
    on_off_switch = not on_off_switch

def move_dxy(x, y):
    mouse.move(x,y,absolute=False,duration=SAMPLERATE)

def move_array_dxy(move_list):
    for move in move_list:
        move_dxy(move[0], move[1])

if __name__ == "__main__":
    keyboard.add_hotkey('/', lambda: toggle())
    time.sleep(1)
    i = 0

    mov_list = []
    for a in range(50):
        mov_list.append([0,5])
    for a in range(50):
        mov_list.append([0,-5])

    while(True):
        time.sleep(0.01)
        if (on_off_switch):
            move_array_dxy(mov_list)
            print("complete", i)
