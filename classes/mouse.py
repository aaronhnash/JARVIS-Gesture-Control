from os import putenv
import pyautogui
from time import sleep


class Mouse():
    """Helper class. Cleanly implements a way to control and track what the mouse is doing."""

    def __init__(self):
        self.width = pyautogui.size()[0]
        self.height = pyautogui.size()[1]
        self.x = pyautogui.position()[0]
        self.y = pyautogui.position()[1]
        self.sense = 1
        self.x_adjust = 0
        self.y_adjust = 0
    
    def get_pos(self):
        return pyautogui.position()
        

    def move_to(self, x,y):
        """Instantly 'teleports' the mouse to a specific location."""
        if (x,y) != (None, None):
            pyautogui.moveTo(self.sense*(x+self.x_adjust),self.sense*(y+self.y_adjust))

    def move(self, x,y):
        """Moves the mouse relative to current position."""
        if (x,y) != (None, None):
            pyautogui.move(x*self.sense+self.x_adjust,y*self.sense+self.y_adjust)

    def update(self):
        """Internal updater. Set to constantly keep track of constants."""
        self.x, self.y = self.get_pos()



    
#mouse = Mouse()
#print("Hello, world!")
#print(f"Width: {mouse.width} Height: {mouse.height}")

#while 1:
    #print(f"X: {mouse.x} Y: {mouse.y}")
    #mouse.update()