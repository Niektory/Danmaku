# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from deck import Deck

class RoleDeck(Deck):
	def __init__(self, players, simplified=False):
		Deck.__init__(self)

		partner_deck = PartnerDeck(players, simplified)
		stage_boss_deck = StageBossDeck(players, simplified)
		ex_boss_deck = ExBossDeck(players, simplified)
		
		self.deck = ["heroine", stage_boss_deck.draw(), stage_boss_deck.draw(), ex_boss_deck.draw()]
		if players >= 5:
			self.deck.append(partner_deck.draw())
		if players >= 6:
			self.deck.append(stage_boss_deck.draw())
		if players >= 7:
			self.deck.append(partner_deck.draw())
		if players == 8:
			self.deck.append("rival")

		self.shuffle()


class PartnerDeck(Deck):
	def __init__(self, players, simplified=False):
		Deck.__init__(self)

		self.deck = []
		if players >= 5:
			self.deck.extend(("partner", "partner"))
			if not simplified:
				self.deck.append("ex midboss")
		if players >= 7 and not simplified:
			self.deck.append("one true partner")

		self.shuffle()


class StageBossDeck(Deck):
	def __init__(self, players, simplified=False):
		Deck.__init__(self)

		self.deck = ["stage boss", "stage boss", "stage boss"]
		if players >= 5 and not simplified:
			self.deck.extend(("final boss", "challenger", "anti-heroine"))

		self.shuffle()


class ExBossDeck(Deck):
	def __init__(self, players, simplified=False):
		Deck.__init__(self)

		self.deck = ["ex boss"]
		if not simplified:
			self.deck.append("phantom boss")

		self.shuffle()
