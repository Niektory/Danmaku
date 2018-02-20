# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from deck import Deck

class MainDeck(Deck):
	def __init__(self, discard_pile):
		Deck.__init__(self, "Main Deck")
		self.deck = ["1up", "1up", "bomb", "bomb", "bomb", "bomb", "capture spell card",
			"focus", "focus", "focus", "graze!", "graze!", "graze!", "graze!", "graze!",
			"graze!", "graze!", "graze!", "graze!", "graze!", "graze!", "graze!", "grimoire",
			"grimoire", "Kourindou", "Kourindou", "laser shot", "last word", "master plan",
			"melee", "mini-hakkero", "party", "power", "power", "power", "power", "power",
			"power", "seal away", "seal away", "seal away", "seal away", "shoot!", "shoot!",
			"shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!",
			"shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!",
			"shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "shoot!", "sorcerer's sutra scroll",
			"spiritual attack", "spiritual attack", "spiritual attack", "spiritual attack",
			"spiritual attack", "spiritual attack", "stopwatch", "supernatural border",
			"supernatural border", "tempest", "Voile", "borrow", "borrow"]
		self.shuffle()
		self.discard_pile = discard_pile

	def draw(self):
		try:
			return Deck.draw(self)
		except IndexError:
			print("Everyone: Main Deck empty; making a new one from the cards in the discard pile")
			self.deck = self.discard_pile.deck
			self.discard_pile.deck = []
			self.shuffle()
			return Deck.draw(self)
