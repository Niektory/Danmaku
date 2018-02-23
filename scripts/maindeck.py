# -*- coding: utf-8 -*-
# Copyright 2018 Tomasz "Niektóry" Turowski

from __future__ import print_function

import copy

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
	Action = None
	Reaction = None
	Item = None
	danmaku = False


class ActionBase(object):
	@staticmethod
	def conditionsSatisfied(state):
		return False

	@staticmethod
	def illegalPlay(state):
		return False

	@staticmethod
	def payCosts(state):
		pass


class ItemBase(object):
	pass


class OneUp(MainDeckCard):
	ID = "1up"
	name = "1UP"
	# healing
	# action [target player]
	# > [that player] gains 1 life
	# reaction [player reduced to 0 life]
	# > [that player] gains 1 life

class Bomb(MainDeckCard):
	ID = "bomb"
	name = "Bomb"
	# invocation
	# > activate spell card
	# reaction [danmaku card played]
	# > cancel [that card]
	# reaction [spell card activated]
	# > cancel [that spell card]

class Borrow(MainDeckCard):
	ID = "borrow"
	name = '"Borrow"'
	# action [target item]
	# > gain control of [that item]

class CaptureSpellCard(MainDeckCard):
	ID = "capture spell card"
	name = "Capture Spell Card"
	# invocation [target player]
	# > activate [that player]'s spellcard

class Focus(MainDeckCard):
	ID = "focus"
	name = "Focus"
	# defense
	# item
	# > passive: [owner] has +2 distance

class Graze(MainDeckCard):
	ID = "graze"
	name = "Graze"
	# dodge
	# reaction [owner attacked]
	# > avoid [that attack]
	# reaction [other player attacked][discard target danmaku card]
	# > avoid [that attack]

class Grimoire(MainDeckCard):
	ID = "grimoire"
	name = "Grimoire"
	# action
	# > [owner] draws 2 cards

class Kourindou(MainDeckCard):
	ID = "kourindou"
	name = "Kourindou"
	# action [discard any number of cards]
	# > draw 1 + [number of discarded cards]

class LaserShot(MainDeckCard):
	ID = "laser shot"
	name = "Laser Shot"
	# danmaku
	# action [target player]
	# > unavoidable attack [that player]

class LastWord(MainDeckCard):
	ID = "last word"
	name = "Last Word"
	# danmaku
	# action
	# > attack [all other players]

class MasterPlan(MainDeckCard):
	ID = "master plan"
	name = "Master Plan"
	# action
	# > resolve [current incident]
	# > look at the top 3 cards of [target deck], place them on the [top or bottom] in [any order]

class Melee(MainDeckCard):
	ID = "melee"
	name = "Melee"
	# danmaku
	# action [target player]
	# > attack [that player]
	# > [that player] can [discard target danmaku card] to copy this action

class MiniHakkero(MainDeckCard):
	ID = "mini hakkero"
	name = "Mini-Hakkero"
	# artifact
	# item
	# > passive: [owner] has +3 range
	# > action [discard 2 cards]
	# >> activate spell card

class Party(MainDeckCard):
	ID = "party"
	name = "Party"
	# action
	# > temp draw [number of active players] cards
	# > for each active player place [one of the drawn cards] in their hand
	# > draw a card

class Power(MainDeckCard):
	ID = "power"
	name = "Power"
	# powerup
	# item
	# > passive: [owner] has +1 range
	# > passive: [owner] has +1 danmaku limit per round

class SealAway(MainDeckCard):
	ID = "seal away"
	name = "Seal Away"
	# danmaku
	# action [target player]
	# > optional: force to discard [target item that player controls]
	# > if [that player] is in range, attack [that player]

class Shoot(MainDeckCard):
	ID = "shoot"
	name = "Shoot"
	danmaku = True
	# danmaku
	# action [discard any number of danmaku cards]
	#     [target player in range (extended by discarded cards)]
	# > attack [that player]

	class Action(ActionBase):
		@staticmethod
		def conditionsSatisfied(state):
			target = state.session.findPlayer(state.message.split(":")[0])
			# check if target is another player
			if not target or target == state.player:
				return False
			temp_hand = copy.deepcopy(state.player.hand)
			# check if all the cards to discard are in hand and of danmaku type
			for to_discard in state.message.split(":")[1:]:
				card = temp_hand.findCard(to_discard)
				if not card or not card.danmaku:
					return False
				temp_hand.deck.remove(card)
			# check if in range (modified by number of discarded cards)
			if state.session.distance(state.player, target) \
					<= state.player.range + state.message.count(":"):
				return True
			return False

		@staticmethod
		def payCosts(state):
			for to_discard in state.message.split(":")[1:]:
				state.player.hand.deck.remove(state.player.hand.findCard(to_discard))

class SorcerersSutraScroll(MainDeckCard):
	ID = "sorcerers sutra scroll"
	name = "Sorcerer's Sutra Scroll"
	# artifact
	# item
	# > on play: draw a card
	# > passive: [owner] draws +1 card during her draw step
	# > passive: [owner] max hand size = 7 (+role modifier)

class SpiritualAttack(MainDeckCard):
	ID = "spiritual attack"
	name = "Spiritual Attack"
	# invocation
	# > activate spell card

class Stopwatch(MainDeckCard):
	ID = "stopwatch"
	name = "Stopwatch"
	# artifact
	# item
	# > passive: [owner] has +1 distance
	# > passive: [owner] has +2 danmaku limit per round

class SupernaturalBorder(MainDeckCard):
	ID = "supernatural border"
	name = "Supernatural Border"
	# defense
	# powerup
	# item
	# > reaction [owner attacked]
	# >> flip the [top card of the deck]
	# >> if [that card] is a spring or summer card, avoid that attack

class Tempest(MainDeckCard):
	ID = "tempest"
	name = "Tempest"
	# action
	# > all players discard their hand and draw 3 cards

class Voile(MainDeckCard):
	ID = "voile"
	name = "Voile"
	# action
	# > draw 3 cards
	# > place a card from your hand on top of the deck

"""
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
"""
DEFAULT_MAIN_DECK = {
	Shoot: 23
}
