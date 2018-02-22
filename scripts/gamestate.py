# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from deck import Deck
from incident import IncidentDeck
from maindeck import MainDeck
from character import CharacterDeck
from role import RoleDeck

SIMPLIFIED = True
CHARACTERS_TO_DRAW = 2

class GameState(object):
	def __init__(self, session):
		self.session = session

	def playerInput(self, name, message):
		pass

# game not started
class PreGame(GameState):
	def run(self):
		pass

# prepare the decks before the game
class InitDecks(GameState):
	def run(self):
		self.session.incident_deck = IncidentDeck()
		self.session.incident = None
		self.session.discard_pile = Deck("discard pile")
		self.session.main_deck = MainDeck(self.session.discard_pile)
		self.session.character_deck = CharacterDeck()
		self.session.role_deck = RoleDeck(len(self.session.players), SIMPLIFIED)

		self.session.state.pop()
		self.session.history.append("init decks")
		self.session.history.append(self.session.incident_deck.deck[:])
		self.session.history.append(self.session.main_deck.deck[:])
		self.session.history.append(self.session.character_deck.deck[:])
		self.session.history.append(self.session.role_deck.deck[:])

# assign roles to all players
class DealRoles(GameState):
	def run(self):
		self.session.history.append("deal roles")
		self.session.state.pop()
		for i, player in enumerate(self.session.players):
			player.role = self.session.role_deck.draw()
			if player.role == "heroine":
				self.session.heroine = player
				self.session.current_player_i = i
			self.session.history.append(player.role)

# deal characters to all players
class DealCharacters(GameState):
	def run(self):
		self.session.state.pop()
		self.session.history.append("deal characters")
		self.session.history.append(CHARACTERS_TO_DRAW)
		dealt_characters = {}
		for i, player in enumerate(self.session.players):
			drawn_characters = []
			for j in xrange(CHARACTERS_TO_DRAW):
				drawn_characters.append(self.session.character_deck.draw())
			dealt_characters[player.name] = drawn_characters
			self.session.history.append(drawn_characters)
		state_choose = ChooseCharacters(self.session)
		state_choose.init(dealt_characters)
		self.session.state.append(state_choose)

# all players need to choose their characters
class ChooseCharacters(GameState):
	def init(self, dealt_characters):
		self.dealt_characters = dealt_characters

	def run(self):
		for player in self.session.players:
			if not player.character:
				return
		self.session.state.pop()
		self.session.history.append("choose characters")
		for player in self.session.players:
			self.session.history.append(player.character)

	def playerInput(self, name, message):
		if message in self.dealt_characters[name]:
			self.session.findPlayer(name).character = message

# reveal the heroine to all players
class RevealHeroine(GameState):
	def run(self):
		self.session.history.append("reveal heroine")
		self.session.history.append(self.session.heroine.name)
		self.session.state.pop()

# deal hands to all players
class DealHands(GameState):
	def run(self):
		for player in self.session.players:
			if player.role == "heroine":
				player.max_hand_size = 5
			else:
				player.max_hand_size = 4
			if player.character == "Patchouli":
				player.max_hand_size += 3
			print("Everyone:", player.name, "has", player.max_hand_size, "max hand size")
			for i in xrange(player.max_hand_size):
				player.hand.append(self.session.main_deck.draw())
			print("Everyone:", player.name, "draws", player.max_hand_size, "cards")
			print(player.name + ": Your hand:", player.hand)

# play the turns
class PlayTurns(GameState):
	def run(self):
		print("Everyone: It's", self.session.current_player.name + "'s turn")

		print("Everyone: Incident Step")
		if not self.session.incident:
			self.session.incident = self.incident_deck.draw()
			print("Everyone:", self.session.incident, "was put into play")

		print("Everyone: Draw Step")
		for i in xrange(2):
			drawn_card = self.session.main_deck.draw()
			self.session.current_player.hand.append(drawn_card)
			print(self.session.current_player.name + ": You drew", drawn_card)
		print("Everyone:", self.session.current_player.name, "draws 2 cards")

		print("Everyone: Main Step")
		while len(self.session.current_player.hand) > 0:
			print(self.session.current_player.name + ": Your hand:")
			for i,card in enumerate(self.session.current_player.hand):
				print("[" + str(i) + "]", card)
			print(self.session.current_player.name
				+ ": Choose a card to play, or press [Enter] to end turn")
			player_input = raw_input()
			if player_input == "":
				break
			try:
				if int(player_input) < 0:
					raise IndexError()
				played_card = self.session.current_player.hand[int(player_input)]
			except (IndexError, ValueError):
				print(self.session.current_player.name
					+ ": Invalid input, enter an integer between 0 and",
					len(self.session.current_player.hand)-1)
			else:
				print("Everyone:", self.session.current_player.name, "plays", played_card)
				self.session.current_player.hand.remove(played_card)
				self.session.discard_pile.deck.append(played_card)
		print("Everyone:", self.session.current_player.name, "ends turn")

		print("Everyone: Discard Step")
		for player in self.session.active_players:
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
					self.session.discard_pile.deck.append(discarded_card)

		while True:
			self.session.current_player_i \
				= (self.session.current_player_i + 1) % len(self.session.players)
			if not self.session.current_player.defeated:
				break
