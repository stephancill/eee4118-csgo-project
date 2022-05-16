import mouse 
import time

if __name__ == "__main__":
    mouse.move(50,50, absolute=True)

    for i in range(10):
        mouse.move(50,50, absolute=False)
        time.sleep(0.01)