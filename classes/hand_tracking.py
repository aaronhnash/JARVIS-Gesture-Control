import cv2

# For this tutorial, I need OpenCV & MediaPipe. 
# cv2 is what runs the recognition software, 
# MediaPipe runs the hand recognition itself.
# MediaPipe is a pre-trained framework developed
# by Google.

import mediapipe as mp
import numpy as np
import time
import joblib

class HandTracker():
    """Helper class for the hand tracker. Keeps everything nice and tidy."""
    
    def __init__(self, has_classifier=False):
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        self.hands = mp_hands.Hands() # The mediapipe class that keeps track of hands, how to recognize them, etc.
        self.cap = cv2.VideoCapture(0)

        self.right_hand = None
        self.left_hand = None

        self.right_thumb = None
        self.right_index = None
        self.right_middle = None
        self.right_ring = None
        self.right_pinky = None
        
        self.classifier1 = None
        self.classifier2 = None
        self.classifier3 = None
        self.classifier4 = None
        self.classifier5 = None
        target_classifier = "classifier_9"
        self._has_classifier = has_classifier

        if self._has_classifier:
            self.classifier1 = joblib.load(f"classification/individual_classifiers/{target_classifier}/gesture_classifier_01")
            self.classifier2 = joblib.load(f"classification/individual_classifiers/{target_classifier}/gesture_classifier_02")
            self.classifier3 = joblib.load(f"classification/individual_classifiers/{target_classifier}/gesture_classifier_03")
            self.classifier4 = joblib.load(f"classification/individual_classifiers/{target_classifier}/gesture_classifier_04")
            self.classifier5 = joblib.load(f"classification/individual_classifiers/{target_classifier}/gesture_classifier_05")




    def main(self):
        """The main loop. This is the threaded entry point. """
        while 1:
            time.sleep(0.001)
            self.update()
            

    def set_hands(self, results):
        if results.multi_hand_landmarks is not None: # Are there any detected hand landmarks?

            #print(results.multi_handedness)
            # Returns a list of detected hands: A left and a right hand. Format:

            """[
                classification { 
                    index: 0
                    score: n
                    label: "Left" 
                }, 
                classification {
                    index: 1
                    score: n
                    label: "Right" 
                }
            ]
            """

            number_of_hands = len(results.multi_handedness)
            for n in range(number_of_hands):
                #print(results.multi_handedness[n])
                if results.multi_handedness[n].classification[0].label == "Right":
                    self.right_hand = results.multi_hand_landmarks[n].landmark
                    if number_of_hands == 1:
                        self.left_hand = None
                else:
                    self.left_hand = results.multi_hand_landmarks[n].landmark
                    if number_of_hands == 1:
                        self.right_hand = None

    def get_gesture(self, q):
        """The 21 hand landmarks.
            WRIST = 0
            THUMB_CMC = 1
            THUMB_MCP = 2
            THUMB_IP = 3
            THUMB_TIP = 4
            INDEX_FINGER_MCP = 5
            INDEX_FINGER_PIP = 6
            INDEX_FINGER_DIP = 7
            INDEX_FINGER_TIP = 8
            MIDDLE_FINGER_MCP = 9
            MIDDLE_FINGER_PIP = 10
            MIDDLE_FINGER_DIP = 11
            MIDDLE_FINGER_TIP = 12
            RING_FINGER_MCP = 13
            RING_FINGER_PIP = 14
            RING_FINGER_DIP = 15
            RING_FINGER_TIP = 16
            PINKY_MCP = 17
            PINKY_PIP = 18
            PINKY_DIP = 19
            PINKY_TIP = 20
        """
        # GESTURES FOR ONE HAND:
        # Track mouse movement
        #   Track mouse using wrist or base of finger instead of tip (if tip is extended, then track movement. otherwise, stay still)
        #   Issue: Might give trouble when trying to drag stuff around 
        # Left click
        #   Track pointer tip relative to third segment--if the get close enough together, then it's a "click"
        # Right click
        #   Same, track pointer and middle finger instead 
        # Drag (separate?)
        # 
        # GESTURES FOR TWO HANDS
        # Zoom
        # Scroll?
        # 
        # Possible ways to manage the gestures:
        # 1) Track movement over a quarter of a second (list of 25 pieces?)

        # If the pointer finger is stretched out, then follow it.
        
        # 
        if self._has_classifier:
            self.set_fingers()
        
        if q is not None:
            if self.right_index == 1 and not self.right_middle==1:
                # if it's extended, then move the pointer.
                x,y = self.get_pointer()
                q.put(["follow", (x,y)])
            
            if self.right_index == 0:
                q.put(["click"])

            #if (self.right_index == 0) and (self.right_middle == 0):
            #    q.put(["rclick"])
            #    print("requesting 'rclick'")

    def get_pointer(self):
        x,y = None,None
        if self.right_hand is not None:
            #if self.right_index == "extended":
            h,w,c = self.img.shape
            x,y = int(self.right_hand[5].x*w), int(self.right_hand[5].y*h)


        return x,y

    def set_fingers(self):
        # Get the data for the landmarks!
        # Key indexes: 1,3,4,5,6,7,9,10,11,13,14,15,17,18,19
        def add_to_row(finger, targetList):
            targetList.append(finger.x)
            targetList.append(finger.y)
            targetList.append(finger.z)
        if self.right_hand is not None:
            request1 = []
            request2 = []
            request3 = []
            request4 = []
            request5 = []

            add_to_row(self.right_hand[1],request1)
            add_to_row(self.right_hand[3],request1)
            add_to_row(self.right_hand[4],request1)

            add_to_row(self.right_hand[5],request2)
            add_to_row(self.right_hand[6],request2)
            add_to_row(self.right_hand[7],request2)

            add_to_row(self.right_hand[9],request3)
            add_to_row(self.right_hand[10],request3)
            add_to_row(self.right_hand[11],request3)

            add_to_row(self.right_hand[13], request4)
            add_to_row(self.right_hand[14], request4)
            add_to_row(self.right_hand[15], request4)

            add_to_row(self.right_hand[17], request5)
            add_to_row(self.right_hand[18], request5)
            add_to_row(self.right_hand[19], request5)

            # Reshape the data to say that it's a 1-dimension feature in a 2D test (AKA, tell it that we're only predicting one sample at a time)

            fitted_request1 = np.array(request1).reshape(1,-1)
            fitted_request2 = np.array(request2).reshape(1,-1)
            fitted_request3 = np.array(request3).reshape(1,-1)
            fitted_request4 = np.array(request4).reshape(1,-1)
            fitted_request5 = np.array(request5).reshape(1,-1)
            
            # Don't currently have a working thumb or pinky model.
            self.right_thumb = self.classifier1.predict(fitted_request1)
            self.right_index = self.classifier2.predict(fitted_request2)
            self.right_middle = self.classifier3.predict(fitted_request3)
            self.right_ring = self.classifier4.predict(fitted_request4)
            self.right_pinky = self.classifier5.predict(fitted_request5)

            #print(self.right_index, self.right_middle, self.right_ring)
            #print(status1, status2, status3, status4, status5)

    def debug(self):
        print(f"Thumb: {self.right_thumb}, Index: {self.right_index}, Middle: {self.right_middle}, Ring: {self.right_ring}, Pinky: {self.right_pinky}")
        

    def update(self, q=None):

        success, self.img = self.cap.read()
        # Flip the image so it can detect left and right properly
        self.img = cv2.flip(self.img, 1)
        

        # convert
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        # this is converting this entire image into rgb
        results = self.hands.process(img_rgb)
        # Process the hands
        self.set_hands(results)
        # Find out what each finger is doing, and if we need any special actions (click, etc.)

        self.get_gesture(q)
