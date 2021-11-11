import cv2

# For this tutorial, I need OpenCV & MediaPipe. 
# cv2 is what runs the recognition software, 
# MediaPipe runs the hand recognition itself.
# MediaPipe is a pre-trained framework developed
# by Google.

import mediapipe as mp
import numpy as np
import time



mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()



# This is the standard "hey look, it's a camera"
# setup for OpenCV. 
cap = cv2.VideoCapture(0)
previous_time = 0
current_time = 0

while True:

    success, img = cap.read()

    # convert
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # this is converting this entire image into rgb
    results = hands.process(img_rgb)

    # print(results.multi_hand_landmarks) # will return information when a hand is detected

    if results.multi_hand_landmarks is not None:
        for hand_lms in results.multi_hand_landmarks: # since it can detect multiple hands, you want to say "do this for each hand"
            for id, landmark in enumerate(hand_lms.landmark): # for each point detected on this hand:
                #print(id, landmark) # where is the hand?

                h,w,c = img.shape

                cx, cy = int(landmark.x*w), int(landmark.y*h)

                print(id, cx, cy) # where's the hand at?

                if id==0: # 4 is the tip of the finger, 0 is the rist
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    # draw a circle at the location of id 0


            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
    
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time



    cv2.putText(img, (f"fps: {str(int(fps))}"), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    cv2.imshow("camera", img)
    cv2.waitKey(1)


