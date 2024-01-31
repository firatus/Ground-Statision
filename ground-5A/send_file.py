import requests
from urllib3 import encode_multipart_formdata
url = "http://192.168.4.1/file"
data = {'title': 'metadata', 'timeDuration': 120}
mp4_f = open("my_video.mp4", 'rb')
files = {'messageFile': mp4_f}
req = requests.post(url, files=files, json=data)
print(req.status_code)


'''with open("my_video.mp4", "rb") as a_file:
    file_dict = {"File": a_file}
    response = requests.post("http://192.168.4.1/file", files=file_dict)
    
print(response.status_code)'''

import requests

'''url = "http://192.168.4.25:1234" # İndirilecek dosyanın URL'si
response = requests.get(url)

with open("dosyaadi.mp4", "wb") as f:
    f.write(response.content)'''
