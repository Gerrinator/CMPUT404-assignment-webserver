#  coding: utf-8 
import socketserver, os


# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Gerard van Genderen
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
        # print("Got a request of: %s\n" % self.data)

        encoder = 'utf-8'
        http_header = 'HTTP/1.1 '
        ok_status = '200 OK'
        redirected = '301 Moved Permanently'

        base_url = "http://127.0.0.1:8080"

        data_read = self.data.decode(encoder).split(' ')
        request_method = data_read[0]
        path = data_read[1]
        # request_path = request_path_string.split('/')
        # request_path.pop(0)
        last_char = path[-1]

        path_ok = True

        if request_method == 'GET':

            fullpath = os.path.abspath('www') + path

            if path.find('..') != -1:
                # Big no-no, return 404
                path_ok = False

            if not os.path.exists(fullpath):
                path_ok = False

            if os.path.isfile(fullpath):
                file_type = path.split('.')[1]

            else:
                file_type = 'dir'

            if path_ok:
                if file_type == 'dir':
                    # First check if the path has an ending slash
                    if last_char == '/':
                        fullpath += 'index.html'
                        self.serve_html(http_header, fullpath, ok_status)
                    else:
                        # 301 if there is no slash
                        path += '/'
                        data_to_send = http_header + redirected + "\r\n" + "Location: " + base_url + path + "\r\n\r\n"
                        self.request.sendall(data_to_send.encode())

                elif file_type == 'html':
                    self.serve_html(http_header, fullpath, ok_status)

                elif file_type == 'css':
                    self.serve_css(http_header, fullpath, ok_status)

            else:
                self.error_not_found(http_header)

        else:
            self.error_bad_method(http_header)

    def error_not_found(self, header):
        data_to_send = header + '404 NOT FOUND' + "\r\n\r\n"
        self.request.sendall(data_to_send.encode())

    def error_bad_method(self, header):
        data_to_send = header + '405 Method Not Allowed' + "\r\n\r\n"
        self.request.sendall(data_to_send.encode())

    def serve_css(self, header, path, code):
        file = open(path)
        data = file.read()
        data_to_send = header + code + "\r\n" + "Content-Type: text/css" + "\r\n\r\n" + data
        self.request.sendall(data_to_send.encode())

    def serve_html(self, header, path, code):
        # print(path)
        file = open(path)
        data = file.read()
        data_to_send = header + code + "\r\n" + "Content-Type: text/html" + "\r\n\r\n" + data
        self.request.sendall(data_to_send.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
