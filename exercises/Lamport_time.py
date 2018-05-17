import time
from threading import Thread
from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

our_id = rank
other_id = 1 if rank == 0 else 0


clock = 0

def other_id_generator():
    global our_id,size
    while True:
        i = random.uniform(0,size)
        if i != our_id:
            return i

def listen(listen_id):
    global clock, size, our_id
    while True:
        req = comm.irecv(source=listen_id, tag=11)
        data = req.wait()
        print "I am {3} listening to {4}. My clock is: {0}. Incoming clock is: {1}. Result is: {2}".format(clock, data["clock"],max(clock,data["clock"]), our_id, listen_id)
        clock = max(clock, data["clock"])

def event():
    global clock
    while True:
        # TODO: UPDATE CLOCK
        clock = clock+1
        data = {"clock": clock, "data": "Some payload"}
        req = comm.isend(data, dest=other_id_generator(), tag=11)
        req.wait()
        time.sleep(1.0 + rank * 0.07)

for i in range(size):
    if i != our_id:
        Thread(target=listen, args=(i, )).start()
event = Thread(target=event).start()


raw_input()


# TODO: What is tag?

'''
    if rank == 0: 
        count = count +1
        data = {'counter': count, 'data': "Payload"}
        req = comm.isend(data, dest=1, tag=11)
        req.wait()
    elif rank == 1: 
        req = comm.irecv(source=0, tag=11)
        data = req.wait()
        print data
'''
