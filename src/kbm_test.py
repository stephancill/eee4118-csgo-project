# import mouse 
import pyautogui
import time
import keyboard

on_off_switch = False

def toggle():
    print("toggle")
    global on_off_switch
    on_off_switch = not on_off_switch

if __name__ == "__main__":
    keyboard.add_hotkey('/', lambda: toggle())
    time.sleep(1)
    i = 0
    while(True):
        time.sleep(0.01)
        if (on_off_switch):
            i += 1
            # mouse.move(-500,0, absolute=False, duration=1, steps_per_second=5)
            pyautogui.move(-500, 0, duration=1)
            pyautogui.click()

            pyautogui.move(500, 0, duration=1)
            pyautogui.click()

            print("complete", i)
