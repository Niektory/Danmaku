# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

import random

class Deck(object):
	def __init__(self):
		self.deck = []

	def shuffle(self):
		random.shuffle(self.deck)

	def draw(self):
		return self.deck.pop()
