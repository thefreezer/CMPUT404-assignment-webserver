#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        req = self.data.decode("utf-8") # turns request into easily readable format
        method, url = req.split()[0], req.split()[1]
        #print(method, url)

        if method != "GET":
            self.request.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())
            return
        else:
            if url.endswith(".html"):
                mime_type = "text/html"
            elif url.endswith(".css"):
                mime_type = "text/css"
            elif url.endswith("/"): # return index.html(as per requirement)
                url += "index.html"
                mime_type = "text/html"
            else:
                self._404()

            try:
                url = "www" + url
                with open(url, "r") as f:
                    res = "HTTP/1.1 200 OK\r\n"+ "Content-type: "+ mime_type + "\r\n" + f.read()
                    self.request.sendall(res.encode())
                    return
            except: # error finding file
                self._404()
                return
                
              
    def _404(self):
        res = "HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404: File not found</h3><h1></body>"
        self.request.sendall(res.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
