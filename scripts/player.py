# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

DEFAULT_LIFE = 4

class Player(object):
	def __init__(self, name):
		self.name = name
		self.role = None
		self.character = None
		self.life_lost = 0
		self.max_hand_size = 4
		self.hand = []
		self.defeated = False

	@property
	def max_life(self):
		return DEFAULT_LIFE

	@property
	def life(self):
		return self.max_life - self.life_lost

	@life.setter
	def life(self, value):
		self.life_lost = self.max_life - value
