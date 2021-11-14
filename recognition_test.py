from classes.hand_tracking import HandTracker
import joblib
import time

tracker = HandTracker(True)

while 1:
    tracker.update()
    tracker.debug()
    time.sleep(0.01)