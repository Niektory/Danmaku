# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket
import time

from config import version
from network import ClientConnection

class Client(object):
	def run(self):
		print("Welcome to {} {} client!".format(version.game_name, version.version))
		with ClientConnection() as connection:
			while not connection.connection.closed:
				time.sleep(0.05)
				while connection.connection.read():
					pass
				message = raw_input()
				while connection.connection.read():
					pass
				if message == "quit":
					return
				connection.connection.send(message)
