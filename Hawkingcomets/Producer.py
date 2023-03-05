#class producer to produce items into a queue
class Producer:

    #method produce to produce items into a queue
    def produce(queue,args):
        #produce items into queue
        queue.put(args)