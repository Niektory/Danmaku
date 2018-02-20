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
CHARACTERS_TO_DRAW = 2

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
		self.heroine = None
		for i in xrange(PLAYERS):
			new_player = Player()
			new_player.name = "Player " + str(i)
			new_player.role = self.role_deck.draw()
			self.players.append(new_player)
			if new_player.role == "heroine":
				self.heroine = new_player
			print(new_player.name + ": You got role", new_player.role)

		# assign characters to players
		for player in self.players:
			drawn_characters = []
			for i in xrange(CHARACTERS_TO_DRAW):
				drawn_characters.append(self.character_deck.draw())
			print(player.name + ": Choose a character")
			for i,character in enumerate(drawn_characters):
				print("[" + str(i) + "]", character)
			while True:
				player_input = raw_input()
				try:
					if int(player_input) < 0:
						raise IndexError()
					player.character = drawn_characters[int(player_input)]
				except (IndexError, ValueError):
					print(player.name + ": Invalid input, enter an integer between 0 and",
						len(drawn_characters)-1)
				else:
					break
			print(player.name + ": You got character", player.character)
		for player in self.players:
			print("Everyone:", player.name, "has chosen character", player.character)

		# reveal the heroine
		print("Everyone:", self.heroine.name, "is the heroine")

		# set starting life and max life of all players
		for player in self.players:
			if player.role == "heroine":
				player.max_life = 5
			else:
				player.max_life = 4
			player.life = player.max_life
			print("Everyone:", player.name, "has", player.life, "life")
