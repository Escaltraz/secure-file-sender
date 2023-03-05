#import local custom modules
import var, database, zip, fileoperation, AES, clientele, check

#class consumer that removes items from queue
class Consumer:
    #method that removes items from queue
    def consume():
        #infinite while loop that checks for items in queue
        while True:
            #get an item from queue
            f=var.queue.get()

            #get function name
            fname=f[0]

            #execute function parameters
            i=1
            while i<len(f):
                exec(f[i])
                i+=1

            #execute the required function
            exec(fname)