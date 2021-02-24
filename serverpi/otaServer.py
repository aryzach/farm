import http.server
import socketserver
import os

web_dir = os.path.dirname('/home/pi/ota/')
os.chdir(web_dir)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 80
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()
