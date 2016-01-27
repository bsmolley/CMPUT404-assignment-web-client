#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# curl -v -X GET http://softwareprocess.es/static/SoftwareProcess.es.html
# 404Get, 404Post, Get, InternetGets, Post

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        # use sockets!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        #print("Connected")
        return s
        #return None

    def get_code(self, data):
        split = data.split()
        code = split[1]
        #print(data)
        print("CODE HYPE: " + code)
        return int(code)

    def get_headers(self,data):
        return None

    def get_body(self, data):
        new = data.split()
        for i in new:
            print i
        # start = data.find("<head>")
        # end = data.find("</body>")
        # i = start
        # body = ''
        # while i <= end + 6:
        #     body += data[i]
        #     i += 1
        # #print (start, end)
        # print body
        return body

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            #print("Working")
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
            #print(part)
        return str(buffer)

    def GET(self, url, args=None):
        #print(url)
        host, port, path = self.parse_url(url)
        port = self.get_port(port)
        #print host, port, path

        socket = self.connect(host, port)

        # send a request first, sendall??
        if path == "/":
            path = ''
        print("GOT HERE")
        request = "GET %s HTTP/1.1\nHost: %s\nConnection: close\n\n" % (path, host)
        socket.sendall(request)
        #print("Request: " + request)

        response = self.recvall(socket)
        print("Response: " + response)
        
        socket.close()
        code = self.get_code(response)
        #body = self.get_body(response)
        #print(len(body))
        #code = 500
        #body = ''
        body = response
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def parse_url(self, url):
        split = url.split(':')
        print(split)

        if len(split) == 2:
            print("GOT HERE")
            host = split[1].strip('/')
            if '/' in host:
                lst = host.split('/')
                host = lst[0]
                path = ''
                port = ''
                for i in range(1, len(lst)):
                    path += '/' + lst[i]
                print host
            else:
                port = ''
                path = '/'

        elif len(split) == 3:
            host = split[1].strip('/')
            port = split[2].split('/')[0]
            path = split[2].strip(port)

        if path[0] != '/':
            #print("Yup")
            path = '/' + path
        #print("PATH HYPE: " + path)
        print(host, port, path)
        return host, port, path

    def get_port(self, port):
        if (port == ''):
            port = 80
        else:
            port = int(port)

        return port
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )