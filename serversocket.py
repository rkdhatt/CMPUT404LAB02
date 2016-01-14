#!/usr/bin/env python

# Copyright (c) Raman Dhatt

import socket, os, sys, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# listen for incoming connections - bind.
serverSocket.bind(("0.0.0.0", 12345)) # 1st part of tuple: where on computer to listen and on what port. (IP address. Listen to all of them.) 2nd part of tuple must be > 1024

serverSocket.listen(5) # 5 - number of connections to queue before handling them

while True:
	print "Waiting for connection..."
	(incomingSocket, address) = serverSocket.accept() # Once connection reached, socket accepts it.
	print "We got a connection from %s" % (str(address)) 

# do curl localhost:12345 ||| Response: We got a connection from ('127.0.0.1', 51866)
	
	pid = os.fork() # split into 2 programs. 1) get 0 2) some # (process identifier)
	if(pid == 0):
		# We must be in the child process
		outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		outgoingSocket.connect(("www.google.com", 80))
		request = bytearray()
		while True:
			# incomingSocket acts like proxy to the outgoing socket.
			incomingSocket.setblocking(0)
			try:
				part = incomingSocket.recv(1024)
			except IOError, exception:
				if exception.errno == 11:
					part = None # nothing to read, move on.
				else:
					raise						
			if (part):
				request.extend(part)
				outgoingSocket.sendall(part) # Send back what the client sent (talk to yourself)
				#telnet localhost 12345

			outgoingSocket.setblocking(0)
			try:
				part = outgoingSocket.recv(1024)
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise			
			if (part):
				incomingSocket.sendall(part)

			# lowers CPU usage.
			select.select(
					[incomingSocket, outgoingSocket],
					[],
					[incomingSocket, outgoingSocket],
					1.0)
		print request
		sys.exit(0)
	else:
		# We must be in the parent process - move back around and wait for the next connection.
		pass
	

# Note: talking to one socket (1 terminal) at a time without forking.



