# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

import random

class Deck(object):
	def __init__(self, name="deck"):
		self.deck = []
		self.name = name

	def shuffle(self):
		random.shuffle(self.deck)

	def draw(self):
		return self.deck.pop()

	def findCard(self, to_find):
		for card in self.deck:
			if to_find == card.ID:
				return card
