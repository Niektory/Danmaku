# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from player import Player
from deck import Deck
from incident import IncidentDeck
from maindeck import MainDeck
from character import CharacterDeck
from role import RoleDeck

SIMPLIFIED = True
CHARACTERS_TO_DRAW = 2

class GameSession(object):
	def __init__(self):
		self.state = ["waiting for players"]
		self.history = []
		self.players = []

	def addPlayer(self, name):
		if not self.findPlayer(name):
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
		i = player1
		dist1 = 0
		while i % len(self.players) != player2:
			i += 1
			if not self.players[i % len(self.players)].defeated:
				dist1 += 1

		i = player2
		dist2 = 0
		while i % len(self.players) != player1:
			i += 1
			if not self.players[i % len(self.players)].defeated:
				dist2 += 1

		return min(dist1, dist2)

	def start(self):
		# start the game if there's enough players
		#if self.state[-1] == "waiting for players" and 4 <= len(self.players) <= 8:
		if self.state[-1] == "waiting for players":	# for testing
			self.state.pop()
			self.state.extend(("play turns", "deal hands", "init life", "reveal heroine",
				"assign characters", "assign roles", "init decks"))
			self.history.append("start game")
			self.history.append(len(self.players))
			for player in self.players:
				self.history.append(player.name)
			return True
		return False

	def initDecks(self):
		# prepare the decks before the game
		self.incident_deck = IncidentDeck()
		self.incident = None
		self.discard_pile = Deck("discard pile")
		self.main_deck = MainDeck(self.discard_pile)
		self.character_deck = CharacterDeck()
		self.role_deck = RoleDeck(len(self.players), SIMPLIFIED)

		self.state.pop()
		self.history.append("init decks")
		self.history.append(self.incident_deck.deck[:])
		self.history.append(self.main_deck.deck[:])
		self.history.append(self.character_deck.deck[:])
		self.history.append(self.role_deck.deck[:])

	def assignRoles(self):
		# assign roles to all players
		self.history.append("assign roles")
		self.state.pop()
		for i, player in enumerate(self.players):
			player.role = self.role_deck.draw()
			if player.role == "heroine":
				self.heroine = new_player
				self.current_player_i = i
			self.history.append(player.role)

	def assignCharacters(self):
		# assign characters to all players
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

	def revealHeroine(self):
		# reveal the heroine to all players
		print("Everyone:", self.heroine.name, "is the heroine")

	def initLife(self):
		# set starting life of all players
		for player in self.players:
			if player.role == "heroine":
				player.max_life = 5
			else:
				player.max_life = 4
			player.life = player.max_life
			print("Everyone:", player.name, "has", player.life, "life and max life")

	def dealHands(self):
		# deal hands to all players
		for player in self.players:
			if player.role == "heroine":
				player.max_hand_size = 5
			else:
				player.max_hand_size = 4
			if player.character == "Patchouli":
				player.max_hand_size += 3
			print("Everyone:", player.name, "has", player.max_hand_size, "max hand size")
			for i in xrange(player.max_hand_size):
				player.hand.append(self.main_deck.draw())
			print("Everyone:", player.name, "draws", player.max_hand_size, "cards")
			print(player.name + ": Your hand:", player.hand)

	def playTurns(self):
		# play the turns
		print("Everyone: It's", self.current_player.name + "'s turn")

		print("Everyone: Incident Step")
		if not self.incident:
			self.incident = self.incident_deck.draw()
			print("Everyone:", self.incident, "was put into play")

		print("Everyone: Draw Step")
		for i in xrange(2):
			drawn_card = self.main_deck.draw()
			self.current_player.hand.append(drawn_card)
			print(self.current_player.name + ": You drew", drawn_card)
		print("Everyone:", self.current_player.name, "draws 2 cards")

		print("Everyone: Main Step")
		while len(self.current_player.hand) > 0:
			print(self.current_player.name + ": Your hand:")
			for i,card in enumerate(self.current_player.hand):
				print("[" + str(i) + "]", card)
			print(self.current_player.name
				+ ": Choose a card to play, or press [Enter] to end turn")
			player_input = raw_input()
			if player_input == "":
				break
			try:
				if int(player_input) < 0:
					raise IndexError()
				played_card = self.current_player.hand[int(player_input)]
			except (IndexError, ValueError):
				print(self.current_player.name
					+ ": Invalid input, enter an integer between 0 and",
					len(self.current_player.hand)-1)
			else:
				print("Everyone:", self.current_player.name, "plays", played_card)
				self.current_player.hand.remove(played_card)
				self.discard_pile.deck.append(played_card)
		print("Everyone:", self.current_player.name, "ends turn")

		print("Everyone: Discard Step")
		for player in self.active_players:
			while len(player.hand) > player.max_hand_size:
				print(player.name + ": Your hand:")
				for i,card in enumerate(player.hand):
					print("[" + str(i) + "]", card)
				print(player.name + ": Choose a card to discard")
				player_input = raw_input()
				try:
					if int(player_input) < 0:
						raise IndexError()
					discarded_card = player.hand[int(player_input)]
				except (IndexError, ValueError):
					print(player.name + ": Invalid input, enter an integer between 0 and",
						len(player.hand)-1)
				else:
					print("Everyone:", player.name, "discards", discarded_card)
					player.hand.remove(discarded_card)
					self.discard_pile.deck.append(discarded_card)

		while True:
			self.current_player_i = (self.current_player_i + 1) % len(self.players)
			if not self.current_player.defeated:
				break

	def run(self):
		if self.state[-1] == "init decks":
			self.initDecks()
		elif self.state[-1] == "assign roles":
			self.assignRoles()
		elif self.state[-1] == "assign characters":
			self.assignCharacters()
		elif self.state[-1] == "reveal heroine":
			self.revealHeroine()
		elif self.state[-1] == "init life":
			self.initLife()
		elif self.state[-1] == "deal hands":
			self.dealHands()
		elif self.state[-1] == "play turns":
			self.playTurns()