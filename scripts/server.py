# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket

from config import version
from network import ServerConnections

class Server(object):
	def run(self):
		print("Welcome to {} {} server!".format(version.game_name, version.version))
		with ServerConnections() as connections:
			message = None
			while message != "shutdown":
				connections.prune()
				connections.accept()
				connections.broadcast()
				message = connections.read()
