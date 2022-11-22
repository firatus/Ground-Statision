# Python program to calculate RTT

import requests
from pythonping import ping


#r = input("Web Site")
'''
url = "https://www.facebook.com/"

p = "8.8.8.8"
x = requests.get(url)

if x.status_code == '200' or '301' or '302':
    print("Website is up")

    print(ping(p.text))

else:
    print("Web Site is down")'''

import socket

ip = socket.gethostbyname('www.facebook.com')
print(ip)




