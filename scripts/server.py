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
			history_processed = 0
			message = None
			while message != "shutdown":
				connections.prune()
				connections.accept()
				connections.broadcast()

				user, message = connections.read()
				# list the players
				if message == "players":
					for player in game_session.players:
						connections.message(user, player.name)
				# game not started yet
				elif game_session.state[-1] == "waiting for players":
					# join the game as player
					if message == "join":
						if game_session.addPlayer(user):
							connections.broadcast("{} joined the game".format(user))
					# start the game with the players that joined so far
					elif message == "start":
						if game_session.start():
							connections.broadcast("Starting a {}-player game"
								.format(len(game_session.players)))

				game_session.run()
				while history_processed < len(game_session.history):
					print("History:", game_session.history[history_processed])
					history_processed += 1
