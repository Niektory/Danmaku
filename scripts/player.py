# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

class Player(object):
	def __init__(self):
		self.name = "anon"
		self.role = "loser"
		self.character = "fairy"
		self.max_life = 4
		self.life = self.max_life
		self.max_hand_size = 4
		self.hand = []
		self.defeated = False
