# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from deck import Deck

class IncidentDeck(Deck):
	def __init__(self):
		Deck.__init__(self)
		self.deck = ["crisis of faith", "crossing to Higan", "endless party", "eternal night",
			"five impossible requests", "great barrier weakening", "great fairy wars",
			"Lily White", "overdrive", "rekindle blazing hell", "Saigyou Ayakashi blooming",
			"scarlet weather rhapsody", "spring snow", "undefined fantastic object",
			"voyage to Makai", "worldly desires"]
		self.shuffle()
