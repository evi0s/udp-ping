"""UDP Ping Server"""
import random
import sys
from socket import *

from debug import *


HOST = '0.0.0.0'
PORT = 62000

# Creat udp socket
debug('Starting server...')
server_socket = socket(AF_INET, SOCK_DGRAM)

# Bind Host and Port
try:
    debug('Binding Host & Port...')
    server_socket.bind((HOST, PORT))
    debug(f'Host: {HOST} PORT: {PORT}')
except OSError as err:
    error(err.args[1])
    sys.exit(0)

try:
    while True:

        # Receive Message
        message, address = server_socket.recvfrom(1024)

        # Get Client ping
        debug(f'Client {address} ping')

        # Generate Random number in order to simulate packet loss
        rand = random.randint(0, 20)
        if rand < 4:
            continue

        # Pong
        server_socket.sendto(message, address)

except KeyboardInterrupt:
    error("KeyboardInterrupt")
    server_socket.close()
    sys.exit(0)
