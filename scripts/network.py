# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket
import select

IP = "127.0.0.1"
PORT = 12347
BUFFER_SIZE = 4096

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

	def prune(self):
		for connection in self.connections[:]:
			if connection.closed:
				self.connections.remove(connection)

	@property
	def active(self):
		return len(self.connections)

	def read(self):
		for connection in self.connections:
			message = connection.read()
			if message:
				return message

	def broadcast(self, message=""):
		for connection in self.connections:
			connection.send(message)

	def __exit__(self, exc_type, exc_value, traceback):
		for connection in self.connections:
			connection.close()
		self.server_socket.close()


class ClientConnection(object):
	def __enter__(self):
		client_socket = socket.socket()
		client_socket.connect((IP, PORT))
		self.connection = Connection(client_socket, (IP, PORT))
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.close()


class Connection(object):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.read_buffer = ""
		self.send_buffer = ""
		self.closed = False

	def read(self):
		# read from the socket and add data to the buffer
		if not self.closed and select.select([self.socket], [], [], 0)[0]:
			try:
				data = self.socket.recv(BUFFER_SIZE)
			except socket.error as msg:
				print("Socket error: {}".format(msg))
				self.close()
			else:
				if data:
					print("Received data:", data)
					self.read_buffer += data
				else:
					self.close()

		# check if we got a complete message
		if len(self.read_buffer) < 3:
			return
		try:
			message_length = int(self.read_buffer[:3])
		except ValueError:
			print("Error: Malformed message")
			self.close()
			return
		if len(self.read_buffer) < 3 + message_length:
			return

		# return a single message
		message, self.read_buffer \
			= self.read_buffer[3:3+message_length], self.read_buffer[3+message_length:]
		print("Message is {}".format(message))
		#self.send(message)	#echo
		return message

	def send(self, message=""):
		# add message to the buffer
		if message:
			if len(str(message)) > 999:
				print("Error: Message too long")
			else:
				self.send_buffer += str(len(str(message))).zfill(3) + str(message)

		# attempt sending the buffer
		if not self.closed and self.send_buffer \
				and select.select([], [self.socket], [], 0)[1]:
			try:
				characters_sent = self.socket.send(self.send_buffer)
			except socket.error as msg:
				print("Socket error: {}".format(msg))
				self.close()
			else:
				if characters_sent:
					self.send_buffer = self.send_buffer[characters_sent:]
				else:
					self.close()

	def close(self):
		if self.closed:
			return
		self.socket.close()
		self.closed = True
		print("{} disconnected".format(self.address))
