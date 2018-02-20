# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from deck import Deck

class CharacterDeck(Deck):
	def __init__(self):
		Deck.__init__(self, "Character Deck")
		self.deck = ["Alice", "Cirno", "Reimu", "Byakuren", "Tenshi", "Meiling", "Suika",
			"Sakuya", "Keine", "Nitori", "Yuuka", "Marisa", "Sanae", "Satori", "Youmu",
			"Futo", "Patchouli", "Reisen", "Utsuho", "Remilia", "Aya", "Miko", "Eirin",
			"Yukari", "Player 2"]
		self.shuffle()
