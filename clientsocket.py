#!/usr/bin/env python

# Copyright (c) Raman

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (SOCKET FOR INTERNET (IP), allows us to use TCP stream)

clientSocket.connect(("www.google.com", 80)) # tell socket to connect to remote server. Make sure you send a tuple argument.

request = "GET / HTTP/1.0\n\n" # 2 newlines completes request

clientSocket.sendall(request)

response = bytearray()
while True:
	part = clientSocket.recv(1024) # specify bytes at a time; get small chunks of data at a time, don't know how much we're getting.
	if (part):
		response.extend(part)
	# else we know we stopped getting bytes.
	else:
		break

print response

