from multiprocessing import Process, Queue
from threading import Thread
import time
import keyboard

class Test1():
    def __init__(self, sleeptime):
        self.count = 0
        self.sleep = sleeptime

    def main(self, q):
        while 1:
            # Should be running in it's own separate process.
            try:
                input_data = q.get(False)
                print(f"At self count {self.count}, input is {input_data}")
            except:
                pass
            time.sleep(self.sleep)
            self.count+=1
            #print("Iterating") # A test statement to see if the main loop is being called. 

class Test2():
    def __init__(self, sleeptime):
        self.count = 0
        self.sleep = sleeptime

    def main(self, q):
        while 1:
            q.put(self.count)
            self.count+=1
            time.sleep(self.sleep)


q = Queue()



if __name__ == "__main__":
    test1 = Test1(1)
    test2 = Test2(1.387)

    # Start thread one
    test1_thread = Process(target=test1.main, args=(q,))
    print("Starting 1")
    test1_thread.start()

    # Start thread two
    test2_thread = Process(target=test2.main, args=(q,))
    print("Starting 2")
    test2_thread.start()

    input()
    

    # count = 0
    # while 1:
    #     #print(f"Main Count {count}: Test1 {test1.count}, Test2 {test2.count}")
    #     count += 1
    #     time.sleep(1)