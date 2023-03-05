#import required module
from queue import Queue

#create GUIqueue for GUI tasks
GUIqueue=Queue()

#create queue for Non GUI based tasks
queue=Queue()

#create a flag variable
flag=False