import sys
# from socket import *
import socket
import time
# from collections import namedtuple
import threading

class Node:
    def __init__(self, router, port, edges, status):
        self.name = router
        self.port = port
        self.edge_weights = edges # dictionary
        self.status = status

UPDATE_INTERVAL = 1

def parse_config(config_file, my_node, graph):
    file = open(config_file)
    text = file.readlines()
    pos = 1
    while pos <= int(text[0]):
        line = text[pos].split()
        my_node.edge_weights.update({line[0] : float(line[1])})
        # neighbour = Node(line[0], line[2], {my_node.name : float(line[1])}, True)
        # graph.append(neighbour)
        pos += 1


# thread a = receives packets
class Receive(threading.Thread):
    def run(self, received):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("127.0.0.1", port))

# thread b = determines if the received packets need to be sent
class Restrict(threading.Thread):
    def run(self, received, restricted):

        
# thread c = retransmits packets from other nodes
class Retransmit(threading.thread):
    def run(self, restricted):

# thread d = sends own packets
class Send(threading.thread):
    def run(self, my_node):

# thread e = dijkstra's algorithm



graph = {}, received = {}, restricted = {}
router_id = str(sys.argv[1])
port = int(sys.argv[2])
config_file = str(sys.argv[3])
my_node = Node(router_id, port, {}, True)
graph.append(my_node)
parse_config(config_file, my_node, graph)
# for i in graph:
#     print(i.__dict__)

receive_packets = Receive()
restrict_transmission = Restrict()