# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

DEFAULT_LIFE = 4

class Player(object):
	def __init__(self, name):
		self.name = name
		self.role = None
		self.character = None
		self.life = DEFAULT_LIFE
		self.max_hand_size = 4
		self.hand = []
		self.defeated = False

	@property
	def max_life(self):
		return DEFAULT_LIFE
