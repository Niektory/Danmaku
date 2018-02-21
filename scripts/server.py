# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import socket

from config import version
from network import ServerConnections
from gamesession import GameSession

class Server(object):
	def run(self):
		print("Welcome to {} {} server!".format(version.game_name, version.version))
		with ServerConnections() as connections:
			game_session = GameSession()
			message = None
			while message != "shutdown":
				connections.prune()
				connections.accept()
				connections.broadcast()
				user, message = connections.read()
				if message == "players":
					for player in game_session.players:
						connections.message(user, player.name)
				elif game_session.state[-1] == "waiting for players":
					if user and message == "join":
						if game_session.addPlayer(user):
							connections.broadcast("{} joined the game".format(user))
