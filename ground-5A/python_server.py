'''from http.server import HTTPServer,BaseHTTPRequestHandler

HOST = "192.168.4.25"
PORT = 1234

class NeuralHTTP(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>Example</title></head><body><p>This is an example of a simple HTML page with one paragraph.</p></body></html>","utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "video/mp4")
        self.end_headers()
        print("Maraba")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open("recevied.mp4", "wb") as f:
            f.write(post_data)
        print(f"File received and saved as received_file.txt")


server = HTTPServer((HOST,PORT),NeuralHTTP)
print(("Server Running"))
print("Server started http://%s:%s" % (HOST, PORT))
server.serve_forever()
server.server_close()'''



from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        print(content_length)
        post_data = self.rfile.read(content_length)
        print("Maraba")
        print(post_data)
        with open("recevied.txt", "w") as f:
            
            f.write(post_data)
            f.close()
            
        print(f"File received and saved as received_file.txt")





def run():
    server_address = ('192.168.4.25', 1234)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print('Starting http...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()