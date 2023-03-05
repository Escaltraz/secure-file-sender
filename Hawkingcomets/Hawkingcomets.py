#import threading module
import threading

#importing custom user modules from local directory
from Consumer import Consumer
import server
from GUI import GUI

#main program
if __name__=='__main__':

    #create a thread to start Server function
    t1=threading.Thread(target=server.Server)
    t1.start()

    #create another thread to start Consume function
    t2=threading.Thread(target=Consumer.consume)
    t2.start()

    #calling main_screen function of GUI class
    GUI.main_screen()
