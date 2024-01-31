# uyduya video yollama
import requests
url = "http://192.168.4.1/file"
data = {'title':'metadata','timeDuration':120}
mp3_f = open('kayit.avi', 'rb')
files = {'messageFile': mp3_f}

req = requests.post(url, files=files, json=data)
print (req.status_code)
print (req.content)
'''
import requests

# Set the URL of the server to which you want to send the file
url = 'http://192.168.4.1/file'

# Open the file you want to send
with open('kayit.avi', 'rb') as f:
    # Set the POST parameters
    files = {'file': f}


    # Send the file using POST
    response = requests.post(url, files=files)

# Check the response status code
if response.status_code == 200:
    print('File successfully sent!')
else:
    print('Error:', response.status_code)
'''

#Komut yollama
import requests


r = requests.post('http://192.168.4.2:9000', data="{'number':2}")

print(r.text)
print(r.status_code)




'''

import socket

 

# Create a client socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

 

# Connect to the server

clientSocket.connect(("127.0.0.1",9090));

 

# Send data to server

data = "Hello Server!";

clientSocket.send(data.encode());

 

# Receive data from server

dataFromServer = clientSocket.recv(1024);

 

# Print to the console

print(dataFromServer.decode());'''