import requests
import  numpy as np
'''
value = "A"
url = 'http://192.168.4.1/komut2'
query = {'field': value}
res = requests.post(url, data=query)
print(res.status_code)


#r = requests.post('https://httpbin.org/post', data={'key': 'value'})
'''
'''import requests

res = requests.post('http://192.168.4.1/komut2', data="A")
if res.text == "":
    print("T")

resp = requests.get("http://192.168.4.1/komut2")
print(resp.text)'''
import requests
r = requests.post('', data="{'number':1}")
print(r.text)