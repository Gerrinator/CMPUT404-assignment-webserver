#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Gerard van Genderen
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
        # print ("Got a request of: %s\n" % self.data)

        dir_path = 'www'
        encoder = 'utf-8'
        ok_status = 'HTTP/1.1 200 OK'
        not_allowed = 'HTTP/1.1 405 Not allowed'
        css_type = 'text/css'
        html_type = 'text/html'

        data_read = self.data.decode(encoder).split(' ')
        filename = data_read[1]

        if filename == '/base.css':
            file = open(os.path.abspath(dir_path) + filename)
            data = file.read()
            data_to_send = ok_status + "\r\n" + "Content-Type: " + css_type + "\r\n\r\n" + data
            self.request.sendall(data_to_send.encode())

        if filename == '/index.html':
            file = open(os.path.abspath(dir_path) + filename)
            data = file.read()
            data_to_send = ok_status + "\r\n" + "Content-Type: " + html_type + "\r\n\r\n" + data
            self.request.sendall(data_to_send.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
