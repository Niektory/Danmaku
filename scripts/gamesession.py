# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from player import Player
import gamestate

class GameSession(object):
	def __init__(self):
		self.state = [gamestate.PlayTurns(self), gamestate.DealHands(self),
			gamestate.InitLife(self), gamestate.RevealHeroine(self),
			gamestate.DealCharacters(self), gamestate.DealRoles(self),
			gamestate.InitDecks(self), gamestate.PreGame(self)]
		self.history = []
		self.players = []

	def addPlayer(self, name):
		# can only add players if the game wasn't started yet
		if isinstance(self.state[-1], gamestate.PreGame) and not self.findPlayer(name):
			self.players.append(Player(name))
			return True
		return False

	def findPlayer(self, to_find):
		for player in self.players:
			if to_find == player.name:
				return player

	@property
	def current_player(self):
		return self.players[self.current_player_i]

	@property
	def active_players(self):
		return [player for player in self.players if not player.defeated]

	def distance(self, player1, player2):
		i = self.players.index(player1)
		dist1 = 0
		while i % len(self.players) != self.players.index(player2):
			i += 1
			if not self.players[i % len(self.players)].defeated:
				dist1 += 1

		i = self.players.index(player2)
		dist2 = 0
		while i % len(self.players) != self.players.index(player1):
			i += 1
			if not self.players[i % len(self.players)].defeated:
				dist2 += 1

		return min(dist1, dist2)

	def start(self):
		# start the game if there's enough players
		#if self.state[-1] == "waiting for players" and 4 <= len(self.players) <= 8:
		if isinstance(self.state[-1], gamestate.PreGame):	# for testing
			self.state.pop()
			self.history.append("start game")
			self.history.append(len(self.players))
			for player in self.players:
				self.history.append(player.name)
			return True
		return False

	def run(self):
		self.state[-1].run()

	def playerInput(self, name, message):
		self.state[-1].playerInput(self.findPlayer(name), message)
