"""
Game handles the flow of play
"""

import collections
import random

from . import dealer, hand
from .card import Card
from .move import Move
from .result import Result
from .suit import Suit
from .value import Value


def generate_deck():
    deck = collections.deque()
    for suit in Suit:
        for value in Value:
            card = Card(suit, value)
            deck.append(card)
    random.shuffle(deck)
    return deck


class Game:

    def new_hand(self, player, deck=generate_deck(), dealer=dealer.Dealer()):
        """
        Deals a new hand, plays the game, and returns a tuple of a result and the net change to bankroll
        Order of operations:
            player antes
            Deal cards to dealer
            Deal cards to player
            Until both players have STAND on all hands, or player has busted:
                Accept Player move
                Accept dealer move
            Dealer reveals hidden card
            Resolve the hand
            Update player
            Save stats
        :return:
        """
        bet = player.ante()
        player.take_turn(deck)
        dealer.take_turn(deck)
        player.take_turn(deck)
        dealer.take_turn(deck)
        while True:
            player_turn = player.take_turn(deck, hand)
            dealer_turn = dealer.take_turn(deck, hand)
            if player_turn == Move.DOUBLE_DOWN:
                player.ante(bet=bet)
                bet *= 2
            if (
                player_turn == Move.STAND or player_turn == Move.DOUBLE_DOWN
            ) and dealer_turn == Move.STAND:
                break
            if player.has_busted() or dealer.has_busted():
                break
            dealer.reveal_hand()
            result = self.evaluate(player.get_hand, dealer.get_hand)
            return result, bet if result == Result.VICTORY else -bet

    def evaluate(self, player_hand, dealer_hand):
        return True
