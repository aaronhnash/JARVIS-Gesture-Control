# Program entry point.

from classes.hand_tracking import HandTracker
from classes.mouse import Mouse
import time

from multiprocessing import Process, Queue

if __name__ == "__main__":
    tracker = HandTracker(True)
    mouse = Mouse()
    mouse.sense=1.3

    q = Queue()
    
    #tracker_process = Process(target=tracker.update, args=(q,))
    #mouse_process = Process(target=mouse.update, args=(q,))
    #tracker_process.start()
    #mouse_process.start()


    while 1:
        time.sleep(0.00001) #refresh rate
        tracker.update(q)
        mouse.update(q)
        