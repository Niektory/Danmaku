# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

from deck import Deck

class MainDeck(Deck):
	def __init__(self, discard_pile):
		Deck.__init__(self, "Main Deck")
		self.deck = []
		for card, number in DEFAULT_MAIN_DECK.iteritems():
			for i in xrange(number):
				self.deck.append(card)
		self.shuffle()
		self.discard_pile = discard_pile

	def draw(self):
		try:
			return Deck.draw(self)
		except IndexError:
			print("Main Deck empty; making a new one from the cards in the discard pile")
			self.deck = self.discard_pile.deck
			self.discard_pile.deck = []
			self.shuffle()
			return Deck.draw(self)


class MainDeckCard(object):
	pass


class OneUp(MainDeckCard):
	ID = "1up"
	name = "1UP"

class Bomb(MainDeckCard):
	ID = "bomb"
	name = "Bomb"

class Borrow(MainDeckCard):
	ID = "borrow"
	name = '"Borrow"'

class CaptureSpellCard(MainDeckCard):
	ID = "capture spell card"
	name = "Capture Spell Card"

class Focus(MainDeckCard):
	ID = "focus"
	name = "Focus"

class Graze(MainDeckCard):
	ID = "graze"
	name = "Graze"

class Grimoire(MainDeckCard):
	ID = "grimoire"
	name = "Grimoire"

class Kourindou(MainDeckCard):
	ID = "kourindou"
	name = "Kourindou"

class LaserShot(MainDeckCard):
	ID = "laser shot"
	name = "Laser Shot"

class LastWord(MainDeckCard):
	ID = "last word"
	name = "Last Word"

class MasterPlan(MainDeckCard):
	ID = "master plan"
	name = "Master Plan"

class Melee(MainDeckCard):
	ID = "melee"
	name = "Melee"

class MiniHakkero(MainDeckCard):
	ID = "mini hakkero"
	name = "Mini-Hakkero"

class Party(MainDeckCard):
	ID = "party"
	name = "Party"

class Power(MainDeckCard):
	ID = "power"
	name = "Power"

class SealAway(MainDeckCard):
	ID = "seal away"
	name = "Seal Away"

class Shoot(MainDeckCard):
	ID = "shoot"
	name = "Shoot"

class SorcerersSutraScroll(MainDeckCard):
	ID = "sorcerers sutra scroll"
	name = "Sorcerer's Sutra Scroll"

class SpiritualAttack(MainDeckCard):
	ID = "spiritual attack"
	name = "Spiritual Attack"

class Stopwatch(MainDeckCard):
	ID = "stopwatch"
	name = "Stopwatch"

class SupernaturalBorder(MainDeckCard):
	ID = "supernatural border"
	name = "Supernatural Border"

class Tempest(MainDeckCard):
	ID = "tempest"
	name = "Tempest"

class Voile(MainDeckCard):
	ID = "voile"
	name = "Voile"


DEFAULT_MAIN_DECK = {
	OneUp: 2,
	Bomb: 4,
	CaptureSpellCard: 1,
	Focus: 3,
	Graze: 12,
	Grimoire: 2,
	Kourindou: 2,
	LaserShot: 1,
	LastWord: 1,
	MasterPlan: 1,
	Melee: 1,
	MiniHakkero: 1,
	Party: 1,
	Power: 7,
	SealAway: 4,
	Shoot: 23,
	SorcerersSutraScroll: 1,
	SpiritualAttack: 6,
	Stopwatch: 1,
	SupernaturalBorder: 2,
	Tempest: 1,
	Voile: 1,
	Borrow: 2
}
