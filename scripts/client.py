# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket

IP = "127.0.0.1"
PORT = 12346
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

class Client(object):
	def run(self):
		s = socket.socket()
		s.connect((IP, PORT))
		s.send(MESSAGE)
		data = s.recv(BUFFER_SIZE)
		s.close()

		print("received data:", data)
