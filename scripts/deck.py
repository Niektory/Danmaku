# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import random

class Deck(object):
	def __init__(self, name="deck"):
		self.deck = []
		self.name = name

	def shuffle(self):
		random.shuffle(self.deck)

	def draw(self):
		return self.deck.pop()
