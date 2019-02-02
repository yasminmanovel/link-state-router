# Python 3
import os, sys, threading, time
from socket import *

class Node():
    def __init__(self, router, port, edges, status):
        self.name = router
        self.port = port
        self.num_neighbours = 0
        self.neighbours = edges # dictionary
        self.status = status
        self.time = time.time()

UPDATE_INTERVAL = 1

def parse_config(config_file, my_node, graph):
    file = open(config_file)
    text = file.readlines()
    pos = 1
    my_node.num_neighbours = int(text[0])
    while pos <= my_node.num_neighbours:
        line = text[pos].split()
        my_node.neighbours.update({line[0] : float(line[1])})
        neighbours_ports.update({line[0] : int(line[2])})
        pos += 1


def add_new_node(packet):
    pass

# thread a = receives packets
class Receive(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.end = False
    def run(self):
        while not self.end:
            server_socket = socket(AF_INET, SOCK_DGRAM)
            server_socket.bind(("127.0.0.1", port))
            print("Received:")
            print(server_socket.recv(2000))
        # receive data
        # put it in (received = {})
        

# thread b = determines if the received packets need to be sent, and then sends them if they do
class Restrict(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.end = False
    def run(self):
        while not self.end:
            for node in received:
                if node == my_node.name: continue
                if received.get(node) == restricted.get(node) and restricted.get(node) != None: continue
                # add it to the graph if new/update data
                if (received.get(node.name)) == None:
                        add_new_node(received[node])
                else:
                    restricted[node.name] = received[node.name]
                    # update time and status a packet has been received from that node - for node failures
                    graph[node].time = time.time()
                # send packet
                for n_port in neighbours_ports.values():
                    neighbours_socket = socket(AF_INET, SOCK_DGRAM)
                    neighbours_socket.connect(("127.0.0.1", n_port))
                    neighbours_socket.send(restricted[node].encode())
                    neighbours_socket.close()
        

# thread c = sends own packets
class Send(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.end = False
    def run(self):
        while not self.end:
            # send packet
            link_state_packet = my_node.name + "\n" + config_txt + str(time.time())
            for n_port in neighbours_ports.values():
                neighbours_socket = socket(AF_INET, SOCK_DGRAM)
                neighbours_socket.connect(("127.0.0.1", n_port))
                print("Sent:\n" + link_state_packet)
                neighbours_socket.send(link_state_packet.encode())   
                neighbours_socket.close()             
        
                time.sleep(1)


# thread d = dijkstra's algorithm
class Djikstra(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.end = False
    def run(self):
        while not self.end:
            time.sleep(30)
            # create adjacency matrix based on nodes that haven't failed
            # create vertex set
            Q = {}; dist = {}; prev = []
            # for each vertex in matrix
            i = 0
            for v in graph.values():
                # dist[v] = infinity
                dist.update({v.name : float("inf")})
                Q.update({v.name : v.name})
                # prev[v] = undefined
                prev[i] = '0'
            # dist[source] = 0
            dist[my_node.name] = 0.0
            # while Q is not empty:
            while Q != {}:
                # u = vertex in Q with min dist[u]
                u = min(dist, key=dist.get)
                # remove u from Q
                Q.pop(u)
                # for each neighbour v of u:
                for v in graph:
                    # alt = dist[u] + length(u, v)
                    alt = dist[u] + graph[u].neighbours[v]
                    # if alt < dist[v]:
                    if alt < dist[u]:
                        # dist[v] = alt
                        dist[v] = alt
                        # prev[v] = u
                        prev[v] = u
            # text = str of what im going to print
            text = "I am Router " + my_node.name + "\n"
            # for each node:
            for v in graph:
                # S = empty sequence
                S = []
                # u = target
                # if prev[u] is defined or u = source:
                    # while u is defined:
                        # insert u at the beginning of S
                        # u = prev[u]
                # create line to print
                text += "Least cost path to router " + v.name + ": " + S + " and the cost is " + dist[v.name] + "\n"
            print(text)
                





graph = {}; received = {}; restricted = {}; neighbours_ports = {}; config_txt = ""
router_id = str(sys.argv[1])
port = int(sys.argv[2])
config_file = str(sys.argv[3])
file = open(config_file)
text = file.readlines()
for line in text:
    config_txt = config_txt + line
my_node = Node(router_id, port, {}, True)
graph.update({my_node.name : my_node})
parse_config(config_file, my_node, graph)
# for i in graph:
#     print(i.__dict__)
# need to initialise dicts to 10 empty elements

# create threads
threads = []
receive_packets = Receive("Thread-1")
threads.append(receive_packets)
# restrict_transmission = Restrict("Thread-2")
send_my_packets = Send("Thread-3")
threads.append(send_my_packets)
# djikstras_algo = Djikstra("Thread-4")
# have a new thread for constantly checking time and determining node failure

# run threads 
receive_packets.start()
# restrict_transmission.start()
send_my_packets.start()
# djikstras_algo.start()
while len(threads) > 0:
    try:
        threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
    except KeyboardInterrupt:
        print("Ctrl-C received")
        for t in threads:
            t.end = True