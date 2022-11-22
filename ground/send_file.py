import requests
from urllib3 import encode_multipart_formdata

'''with open("dene.mp4", "rb") as a_file:
    file_dict = {"dene.mp4": a_file}
    response = requests.post("http://192.168.4.1/file", files=file_dict)

    print(response.text)'''

fields = {
    "foo": "bar",
    "somefile": ("dene.mp4", "contents of somefile"),

}

body, header = encode_multipart_formdata(fields)

with open("dene.mp4", "rb") as a_file:
    file_dict = {"dene.mp4": a_file}
    response = requests.post("http://192.168.4.1/file", files=file_dict)
    
    print(response.text)