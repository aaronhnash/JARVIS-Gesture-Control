import time
from classes.hand_tracking import HandTracker
from classes.mouse import Mouse
import pandas as pd

training_thumb = 0
training_index = 0
training_middle = 0
training_ring = 0
training_pinky = 0

count = 0
samples = 200

class Trainer():
    def __init__(self, csv):
        self.loading_csv = csv

    def gather_data(self,hand):

        def add_to_row(finger):
            new_line.append(finger.x)
            new_line.append(finger.y)
            new_line.append(finger.z)

        def add_results(line):
            line.append(self.training_thumb) #thumb status
            line.append(self.training_index) #index status
            line.append(self.training_middle) #middle status
            line.append(self.training_ring) #ring status
            line.append(self.training_pinky) #pinky status
        
        if hand is not None:
            index = 0
            new_line = []
            add_results(new_line)

            for node in hand:
                #print(node)
                # if index == 0:
                #     add_to_row(hand[index])
                # thumb data
                if index ==1:
                    add_to_row(node)
                elif index ==3:
                    add_to_row(node)
                elif index ==4:
                    add_to_row(node)
                # index data
                elif index ==5:
                    add_to_row(node)
                elif index ==6:
                    add_to_row(node)
                elif index==7:
                    add_to_row(node)
                # middle data
                elif index==9:
                    add_to_row(node)
                elif index==10:
                    add_to_row(node)
                elif index==11:
                    add_to_row(node)
                #ring data
                elif index==13:
                    add_to_row(node)
                elif index==14:
                    add_to_row(node)
                elif index==15:
                    add_to_row(node)
                # pinky data
                elif index==17:
                    add_to_row(node)
                elif index==18:
                    add_to_row(node)
                elif index==19:
                    add_to_row(node)

                index +=1
            
    
            self.loading_csv.loc[len(self.loading_csv)] = new_line


    def set_case(self,case):
        if case == 0:
            self.training_thumb = 1
            self.training_index = 1
            self.training_middle = 1
            self.training_ring = 1
            self.training_pinky = 1
        elif case == 1:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 0
            self.training_ring = 0
            self.training_pinky = 0
        elif case == 2:
            self.training_thumb = 0
            self.training_index = 1
            self.training_middle = 0
            self.training_ring = 0
            self.training_pinky = 0
        elif case == 3:
            self.training_thumb = 0
            self.training_index = 1
            self.training_middle = 1
            self.training_ring = 0
            self.training_pinky = 0
        elif case == 4:
            self.training_thumb = 0
            self.training_index = 1
            self.training_middle = 1
            self.training_ring = 1
            self.training_pinky = 0
        elif case == 5:
            self.training_thumb = 0
            self.training_index = 1
            self.training_middle = 1
            self.training_ring = 1
            self.training_pinky = 1
        elif case == 6:
            self.training_thumb = 1
            self.training_index = 0
            self.training_middle = 0
            self.training_ring = 0
            self.training_pinky = 0
        elif case ==7:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 1
            self.training_ring = 0
            self.training_pinky = 0
        elif case ==8:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 0
            self.training_ring = 1
            self.training_pinky = 0
        elif case ==9:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 0
            self.training_ring = 0
            self.training_pinky = 1
        elif case ==10:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 0
            self.training_ring = 1
            self.training_pinky = 1
        elif case ==11:
            self.training_thumb = 0
            self.training_index = 0
            self.training_middle = 1
            self.training_ring = 1
            self.training_pinky = 1
        
        print(self.training_thumb, self.training_index, self.training_middle, self.training_ring, self.training_pinky)

    def finish(self):
        self.loading_csv.to_csv("new.csv")


tracker = HandTracker()

# mouse = Mouse()
# mouse.sense = 1.25
# mouse.y_adjust = -25
# mouse.x_adjust = -50

# Suggested values:
#   sensitivity: 1.2
#   y offset: -150
#   x offset: -200

loading_csv = pd.read_csv("template.csv")


trainer = Trainer(loading_csv)
n = 0
max = 11
trainer.set_case(n)
input("Press enter to continue...")
while max >= n:
    time.sleep(0.000001)
    tracker.update()
    if tracker.right_hand is not None:
        if count <= samples:
            print(f"collecting {count}/{samples}")
            trainer.gather_data(tracker.right_hand)
            count +=1
        else:
            print(f"finished with case {n}")
            count = 0
            n+=1
            print("Next case:")
            trainer.set_case(n)
            input("Press enter to continue with next case...")
    else:
        print("No input. Passing...")

trainer.finish()


# This is the part where we train a new model!

