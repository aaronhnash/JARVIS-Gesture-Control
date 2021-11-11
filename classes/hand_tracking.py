import cv2

# For this tutorial, I need OpenCV & MediaPipe. 
# cv2 is what runs the recognition software, 
# MediaPipe runs the hand recognition itself.
# MediaPipe is a pre-trained framework developed
# by Google.

import mediapipe as mp
import numpy as np
import time

class HandTracker():
    """Helper class for the hand tracker. Keeps everything nice and tidy."""
    
    def __init__(self):
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        self.hands = mp_hands.Hands() # The mediapipe class that keeps track of hands, how to recognize them, etc.
        self.cap = cv2.VideoCapture(0)

        self.right_hand = None
        self.left_hand = None

        self.right_index = "idle"
        self.right_middle = "idle"
        self.right_thumb = "idle"

        self.tolerance = 0.25

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

    def get_gesture(self):
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
        self.set_fingers()

    def get_pointer(self):
        x,y = None,None
        if self.right_hand is not None:
            #if self.right_index == "extended":
            h,w,c = self.img.shape
            x,y = int(self.right_hand[5].x*w), int(self.right_hand[5].y*h)


        return x,y

    def set_fingers(self):
        if self.right_hand is not None:
            # index finger behavior-- if it's close enough to a straight line, then neat!
            # (y2-y1)/(x2-x1) = m
            # Is the slope between the start of the finger and the first segment close enough to the slope between the first and second segments?

            indx1, indy1 = self.right_hand[5].x, self.right_hand[5].y # The first joint, or the knuckle
            indx2, indy2 = self.right_hand[6].x, self.right_hand[6].y # The second joint
            indm1 = (indy2-indy1)/(indx2-indx1) # slope of the first section

            indx3, indy3 = self.right_hand[7].x, self.right_hand[7].y # Second to last joint, the point before the tip
            indm2 = (indy3-indy2)/(indx3-indx2) # slope of the second segment

            #print("Normal test")
            #print(f"{(-1/indm1)*(1-self.tolerance*1)*0.8} < {indm2} < {(-1/indm1)*(1+self.tolerance)*1.2}")
            if (indm2 >= indm1*(1-self.tolerance)) and (indm2 <= indm1*(1+self.tolerance)):
                # Is the index finger close enough to being straight out?
                self.right_index = "extended"
            elif (indm2 >= (1/indm1)*(1-self.tolerance)*0.8) and ((indm2 <= (1/indm1)*(1+self.tolerance)*1.2)):
                # Curl your finger. See how the first and second segments of your index finger make a near 90 degree angle?
                # Normal: n = -1/m
                self.right_index = "curled"
                print("CURLED")
            else:
                self.right_index = "idle"

            # middle finger


            pass

        

    def update(self):
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
        self.get_gesture()
    
        #print(f"Right hand: {self.right_hand}")
        #print(f"Left hand: {self.left_hand}")