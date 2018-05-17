#! /usr/bin/python

from threading import Thread
import random, time, json
import sys, socket
# Get ID

ID = int(sys.argv[1])
COUNT = int(sys.argv[2])

BASE_PORT = 8000
PORT = BASE_PORT + int(ID)
LEADER = 0

NODELIST = { 1: 0, 2: 0, 3: 0, 4: 0 }

def other_id_generator():
    global ID, COUNT
    while True:
        i = random.uniform(1, COUNT)
        if i != ID:
            return int(i)

def listen_handler(conn):
    data = conn.recv(256)
    parsed_data = json.loads(data)
    if parsed_data["comm"] == "elect":
        pass
    if parsed_data["comm"] == "chatter":
        pass
    NODELIST[int(parsed_data['ID'])] = time.time()
    conn.close()

# Create listener
def listen():
    global PORT,ID
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', PORT))
        sock.listen(4)
        print "listen started {}".format(ID)
        while True:
            conn, addr = sock.accept()
            Thread(target=listen_handler, args=(conn,)).start()
    except:
        print "listen failed in: {}".format(ID)
        print sys.exc_info()

def signal_election_result(id):
    pass

def start_election():
    if ID == COUNT:
        LEADER = ID
        signal_election_result(ID)
    else:
        pass

def send_message(to, msg):
    rec_port = to + BASE_PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', rec_port))
        s.send(msg)
    except:
        print "send failed in: {}".format(ID)
        print sys.exc_info()
        if to == LEADER:
            start_election()
    s.close()

# Create chatterbot
def chatter():
    global BASE_PORT
    print "chatter started {}".format(ID)
    start_election() # Start an election on boot.

    while True:
        rec = other_id_generator()
        data = json.dumps({ "comm": "chatter", "ID": ID })
        send_message(rec, data)
        time.sleep(1.0)


Thread(target=listen).start()
time.sleep(1.0)
Thread(target=chatter).start()

while True:
    try:
        raw_input()
    except:
        pass # ignore

