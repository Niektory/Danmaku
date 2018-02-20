# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket
import select

PORT = 12347
BUFFER_SIZE = 4096
MESSAGE_LENGTH = 20

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
			self.connections.append(Connection(connection, address))

	@property
	def active(self):
		return len(self.connections)

	def processMessages(self):
		for connection in self.connections:
			connection.read()
			connection.send()

	def broadcast(self, message):
		for connection in self.connections:
			connection.send(message)

	def __exit__(self, exc_type, exc_value, traceback):
		for connection in self.connections:
			connection.close()
		self.server_socket.shutdown(socket.SHUT_RDWR)
		self.server_socket.close()


class Connection(object):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.read_buffer = ""
		self.send_buffer = ""
		self.closed = False

	def read(self):
		if not self.closed and select.select([self.socket], [], [], 0)[0]:
			data = self.socket.recv(BUFFER_SIZE)
			if data:
				print("Received data:", data)
				self.send(data)	#echo
				self.read_buffer += data
			else:
				self.close()

		if len(self.read_buffer) < MESSAGE_LENGTH:
			return
		message, self.read_buffer \
			= self.read_buffer[:MESSAGE_LENGTH], self.read_buffer[MESSAGE_LENGTH:]
		print("Message is {}".format(message))
		return message

	def send(self, message=""):
		self.send_buffer += message
		if not self.closed and self.send_buffer \
				and select.select([], [self.socket], [], 0)[1]:
			characters_sent = self.socket.send(self.send_buffer)
			if characters_sent:
				self.send_buffer = self.send_buffer[characters_sent:]
			else:
				self.close()

	def close(self):
		if self.closed:
			return
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
		self.closed = True
		print("{} disconnected".format(self.address))
