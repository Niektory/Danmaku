# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from config import version
from player import Player
from incident import IncidentDeck
from maindeck import MainDeck
from character import CharacterDeck
from role import RoleDeck

PLAYERS = 4
SIMPLIFIED = True

class Application(object):
	def run(self):
		print("Welcome to", version.game_name, version.version, "!")

		print("Preparing the game...")
		# prepare the decks
		self.incident_deck = IncidentDeck()
		self.main_deck = MainDeck()
		self.character_deck = CharacterDeck()
		self.role_deck = RoleDeck(PLAYERS, SIMPLIFIED)

		# create players and give them roles
		self.players = []
		for i in xrange(PLAYERS):
			new_player = Player()
			new_player.role = self.role_deck.draw()
			self.players.append(new_player)
			print("Player", i, "got role", new_player.role)
