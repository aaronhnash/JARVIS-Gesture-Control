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

        self.avg_size = 5

        # Initialize the avg list as something that already has coordinate points.
        self.avg_list = [(self.x, self.y)]*self.avg_size
        
    
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
    
    def click(self):
        pyautogui.click()

    def rclick(self):
        pyautogui.rightClick()

    def move_to_avg(self, x, y):
        """Like move_to, but it takes an average of recent measurements for smoother (if slower) movement."""

        x_sum = 0
        y_sum = 0
        # Delete the first item, add to the end.
        if x is not None:
            self.avg_list.pop(0)
            self.avg_list.append((x,y))

        for pair in self.avg_list:
            x_sum+=pair[0]
            y_sum+=pair[1]
        x_avg = x_sum/self.avg_size
        y_avg = y_sum/self.avg_size

        self.move_to(x_avg,y_avg)

            



    def update(self, q=None):
        """Internal updater. Set to constantly keep track of constants."""

        self.x, self.y = self.get_pos()
        command = None
        try:
            command = q.get(False)
        except:
            pass
        if command is not None:
            if command[0] == "follow":
                self.move_to_avg(command[1][0],command[1][1])
            elif command[0] == "click":
                self.click()
            elif command[0] == "rclick":
                self.rclick()



    
#mouse = Mouse()
#print("Hello, world!")
#print(f"Width: {mouse.width} Height: {mouse.height}")

#while 1:
    #print(f"X: {mouse.x} Y: {mouse.y}")
    #mouse.update()