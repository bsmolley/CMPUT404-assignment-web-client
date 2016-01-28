#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, Brandon Smolley
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

    TERMINATE = "\r\n\r\n"

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        split = data.split()
        code = split[1]
        return int(code)

    def get_headers(self, data):
        header = data.split(self.TERMINATE)[0]
        return header

    def get_get_body(self, data):
        # split o \r\n index 0 = header, 1 = body
        body = data.split(self.TERMINATE)[1]
        return body

    def get_post_body(self, data, args):
        broken = False
        lst = data.split("\n")
        for i in range(0, len(lst)):
            if '{' in lst[i] and '}' in lst[i]:
                for arg in args:
                    if str(arg) not in lst[i]:
                        broken = True
                        break
                if not broken:
                    return lst[i]
        return data

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host, port, path = self.parse_url(url)
        socket = self.connect(host, port)

        if args == None:
            arguments = ""
        else:
            arguments = urllib.urlencode(args)

        request =  "GET %s HTTP/1.1\n"  % path
        request += "Host: %s\n"         % host
        request += "Connection: close" + self.TERMINATE
        request += arguments + self.TERMINATE

        socket.sendall(request)
        response = self.recvall(socket)
        socket.close()
        
        code = self.get_code(response)
        body = self.get_get_body(response)

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        host, port, path = self.parse_url(url)
        socket = self.connect(host, port)

        if args == None:
            arguments = ""
        else:
            arguments = urllib.urlencode(args)

        request =  "POST %s HTTP/1.1\n" % path
        request += "Host: %s\n"         % host
        request += "Content-Type: application/x-www-form-urlencoded\n"
        request += "Content-Length: %s\n" % len(arguments)
        request += "Connection: close" + self.TERMINATE
        request += arguments + self.TERMINATE

        socket.sendall(request)
        response = self.recvall(socket)
        socket.close()

        code = self.get_code(response)
        body = self.get_post_body(response, args)
        
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def parse_url(self, url):
        split = url.split(':')
        host, port, path = '', '', ''
        if len(split) == 2 and "http://" in url:
            host = split[1].strip('/')
            if '/' in host:
                lst = host.split('/')
                host = lst[0]
                port = 80
                path = ''
                for i in range(1, len(lst)):
                    path += '/' + lst[i]
            else:
                port = 80
                path = '/'

        elif len(split) == 3 and 'http://' in url:
            host = split[1].strip('/')
            port = split[2].split('/')[0]
            path = split[2].strip(port)
            port = int(port)

        return host, port, path
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( command, sys.argv[1] )