# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from deck import Deck

DEFAULT_LIFE = 4
DEFAULT_HAND_SIZE = 4

class Player(object):
	def __init__(self, name):
		self.name = name
		self.role = None
		self.character = None
		self.life = DEFAULT_LIFE
		self.hand = Deck()
		self.defeated = False

	@property
	def max_life(self):
		return DEFAULT_LIFE

	@property
	def max_hand_size(self):
		return DEFAULT_HAND_SIZE
