# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket
import select

PORT = 12346
BUFFER_SIZE = 20

class ServerConnections(object):
	def __enter__(self):
		self.connections = []
		self.server_socket = socket.socket()
		self.server_socket.bind(("", PORT))
		self.server_socket.listen(5)
		self.server_socket.setblocking(0)
		return self

	def accept(self):
		while select.select([self.server_socket], [], [], 0)[0]:
			connection, address = self.server_socket.accept()
			print("Connection address:", address)
			self.connections.append(connection)

	@property
	def active(self):
		return len(self.connections)

	def getMessages(self):
		for connection in select.select(self.connections, [], [], 0)[0]:
			data = connection.recv(BUFFER_SIZE)
			if not data:
				print("Disconnected")
				connection.shutdown(socket.SHUT_RDWR)
				connection.close()
				self.connections.remove(connection)
				continue
			print("Received data:", data)
			connection.send(data)	#echo

	def __exit__(self, exc_type, exc_value, traceback):
		for connection in self.connections:
			connection.shutdown(socket.SHUT_RDWR)
			connection.close()
		self.server_socket.shutdown(socket.SHUT_RDWR)
		self.server_socket.close()
