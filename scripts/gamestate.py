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

	def run(self):
		pass

	def playerInput(self, player, message):
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
			dealt_characters[player] = drawn_characters
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

	def playerInput(self, player, message):
		if message in self.dealt_characters[player]:
			player.character = message

# reveal the heroine to all players
class RevealHeroine(GameState):
	def run(self):
		self.session.history.append("reveal heroine")
		self.session.history.append(self.session.heroine.name)
		self.session.state.pop()

# set starting life of all players
class InitLife(GameState):
	def run(self):
		self.session.history.append("init life")
		self.session.state.pop()
		for player in self.session.players:
			player.life = player.max_life
			self.session.history.append(player.life)

# deal hands to all players
class DealHands(GameState):
	def run(self):
		self.session.history.append("deal hands")
		self.session.state.pop()
		for player in self.session.players:
			for i in xrange(player.max_hand_size):
				player.hand.deck.append(self.session.main_deck.draw())
			self.session.history.append(player.hand.deck[:])

# play the turns
class PlayTurns(GameState):
	def run(self):
		self.session.history.append("play turn")
		self.session.history.append(self.session.current_player_i)
		self.session.state.extend((
			EndTurn(self.session),
			DiscardStep(self.session),
			PreDiscardStep(self.session),
			MainStep(self.session),
			PreMainStep(self.session),
			DrawStep(self.session),
			IncidentStep(self.session)
		))

# turn: incident step
class IncidentStep(GameState):
	def run(self):
		self.session.history.append("incident step")
		if not self.session.incident:
			self.session.incident = self.session.incident_deck.draw()
			self.session.history.append(self.session.incident)
		else:
			self.session.history.append("no incident drawn")
		self.session.state.pop()

# turn: draw step
class DrawStep(GameState):
	def run(self):
		self.session.history.append("draw step")
		drawn_cards = []
		for i in xrange(2):
			drawn_cards.append(self.session.main_deck.draw())
		self.session.current_player.hand.deck.extend(drawn_cards)
		self.session.history.append(drawn_cards)
		self.session.state.pop()

# turn: before main step
class PreMainStep(GameState):
	def run(self):
		self.session.history.append("main step")
		self.session.state.pop()

# turn: main step
class MainStep(GameState):
	def playerInput(self, player, message):
		if player != self.session.current_player:
			return
		card = self.session.current_player.hand.findCard(message)
		if card:
			self.session.history.append(message)
			self.session.current_player.hand.deck.remove(card)
			self.session.discard_pile.deck.append(card)
		elif message == "pass":
			self.session.history.append(message)
			self.session.state.pop()

# turn: before discard step
class PreDiscardStep(GameState):
	def run(self):
		self.session.history.append("discard step")
		self.session.state.pop()

# turn: discard step
class DiscardStep(GameState):
	def run(self):
		for player in self.session.active_players:
			if len(player.hand.deck) > player.max_hand_size:
				return
		self.session.state.pop()

	def playerInput(self, player, message):
		if len(player.hand.deck) <= player.max_hand_size:
			return
		card = self.session.current_player.hand.findCard(message)
		if card:
			self.session.history.append((player.name, message))
			player.hand.deck.remove(card)
			self.session.discard_pile.deck.append(card)

# turn: end turn
class EndTurn(GameState):
	def run(self):
		self.session.history.append("end turn")
		self.session.state.pop()
		while True:
			self.session.current_player_i \
				= (self.session.current_player_i + 1) % len(self.session.players)
			if not self.session.current_player.defeated:
				break
