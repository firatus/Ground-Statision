#Send Data


host = "google.com" #Static IP
port = 81

import socket

# Create a client socket
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    (sock.connect((host, port)))

except TimeoutError:
    print("Hi")

