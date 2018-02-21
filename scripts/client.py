# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket

from config import version
from network import ClientConnection

class Client(object):
	def run(self):
		print("Welcome to {} {} client!".format(version.game_name, version.version))
		with ClientConnection() as connection:
			while not connection.connection.closed:
				message = raw_input()
				connection.connection.read()
				if not message:
					return
				connection.connection.send(message)
