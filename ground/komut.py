import requests

url = "http://192.168.4.1/komut2"
data = "key1=value1&key2=value2"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

r = requests.post(url, data=data, headers=headers)

print(r.text)