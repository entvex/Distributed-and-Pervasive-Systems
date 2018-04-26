from threading import Thread
from mpi4py import MPI
import random, time, sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
node_count = comm.Get_size()

our_id = rank
#our_id = int(sys.argv[1])
running = True

leader = -1

def other_id_generator():
    global our_id
    while True:
        i = random.uniform(0, node_count)
        if i != our_id:
            return i

def listen(ID):
    global running
    while running == True:
        req = comm.irecv( tag=11)
        data = req.wait()
        print "{0} received: {1}".format(ID, data)
        if data["ID"] == ID:
            if data["comm"] == "die":
                running = False
                sys.exit()
            elif data["comm"] == "chatter":
                sender = data["ID"]
                data = {"comm": "reply", "ID":ID}
                req = comm.isend(data, dest=sender, tag=11)
            #TODO Implement election related messages.
        

def chatter(ID):
    global running
    while running == True:
        data = {"comm": "chatter", "ID": ID }
        destination = other_id_generator()
        req = comm.isend(data, dest=other_id_generator(), tag=11)
        #TODO: Add reply timeout, to trigger election

        #reply = comm.irecv(source=destination, tag=11)
        #data = reply.wait()
        #print "reply: {0}".format(data)
        time.sleep(1.0)

def event():
    global running
    while running == True and rank == 0:
        raw_input()
        data = {"comm": "die", "ID": our_id}
        destination = other_id_generator()
        req = comm.isend(data, dest=destination, tag=11)


print "Starting process with {0} nodes".format(node_count)
#for i in range(node_count):
Thread(target=listen, args=(our_id, )).start()
Thread(target=chatter, args=(our_id, )).start()

#event()
