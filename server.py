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

        path = os.path.abspath('www')
        encoder = 'utf-8'
        http_header = 'HTTP/1.1 '
        ok_status = '200 OK'
        not_found = '404 NOT FOUND'
        not_allowed = '405 Method Not Allowed'
        redirected = '301 Moved Permanently'

        data_read = self.data.decode(encoder).split(' ')
        # print(data_read)
        request_method = data_read[0]
        request_path_string = data_read[1]
        # print(request_path_string)
        request_path = request_path_string.split('/')
        request_path.pop(0)
        # print(request_path)
        dest = ''

        path_ok = True

        if request_method  == 'GET':

            for file in request_path:
                if file == '..':
                    # Very bad! throwing an error
                    path_ok = False
                    break

                elif file == 'deep':
                    path += '/deep'
                    dest = 'deep'

                elif file == '':
                    path += '/'
                    dest = ''

                else:
                    path += '/' + file
                    dest = file

            print(path)

            if not os.path.exists(path):
                path_ok = False

            if path_ok:
                if dest == 'deep':
                    path += '/index.html'
                    self.serve_html(http_header, path, redirected)

                elif dest == 'index.html':
                    self.serve_html(http_header, path, ok_status)

                elif dest == 'base.css':
                    self.serve_css(http_header, path, ok_status)

                elif dest == '':
                    path += 'index.html'
                    self.serve_html(http_header, path, ok_status)

            else:
                self.error_not_found(http_header)

        else:
            self.error_bad_method(http_header)

    def error_not_found(self, header):
        data_to_send = header + '404 NOT FOUND' + "\r\n"
        self.request.sendall(data_to_send.encode())

    def error_bad_method(self, header):
        data_to_send = header + '405 Method Not Allowed' + "\r\n"
        self.request.sendall(data_to_send.encode())

    def serve_css(self, header, path, code):
        file = open(path)
        data = file.read()
        data_to_send = header + code + "\r\n" + "Content-Type: " + 'text/css' + "\r\n\r\n" + data
        self.request.sendall(data_to_send.encode())

    def serve_html(self, header, path, code):
        file = open(path)
        data = file.read()
        data_to_send = header + code + "\r\n" + "Content-Type: " + 'text/html' + "\r\n\r\n" + data
        self.request.sendall(data_to_send.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
