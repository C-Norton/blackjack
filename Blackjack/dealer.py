"""
The dealer is responsible for their own moves, and the game is responsible for
giving the dealer cards, and requesting a move from the dealer

The dealer should have a hand, which should have the first card face down.
The dealer knows the value of the card

The dealer hits on anything below 17.

The dealer's external interface should consist of


reveal_hand() (flips all cards and prints)
all methods in game_participant.py
"""

import collections
from typing import Optional

from .game_participant import GameParticipant
from .hand import Hand
from .move import Move


class Dealer(GameParticipant):
    def __init__(self, dealer_hand: Optional[Hand] = None):
        """
        __init__ is a method that creates a new Dealer object
        :param dealer_hand: a hand object for the dealer. If None, the dealer will create a new hand. This is
        dependency injection
        """
        super().__init__()

    def reveal_hand(self):
        """
        reveal_hand take the facedown card of the dealer's hand and flips it face up
        :return: None
        """
        pass

    def take_turn(self, deck: collections.deque) -> Move:
        """
        take_turn runs the algorithm for the dealer to select between hit and stand
        :param deck: a deque of card objects
        :return: a move enum representing the dealer's choice
        """
        pass
    def deal_card(self, card):
        """
        deal_card adds a card to the dealer's hand. It is responsible for managing if the card is face up or face down
        """
        pass
