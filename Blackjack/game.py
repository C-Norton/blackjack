"""
Game handles the flow of play
"""

import collections
import random

from . import dealer
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

    def __init__(self):
        self.can_player_move = True

    def deal(self, player, deck, dealer):
        self.can_player_move = True
        player.ante()
        player.deal_card(deck)
        dealer.deal_card(deck)
        player.deal_card(deck)
        dealer.deal_card(deck)

    def play_round(self, player, deck, dealer):
        """play round returns a boolean as to if there should be another round"""
        if self.can_player_move:
            player_turn = player.take_turn(deck)
            if player.get_hand().get_total() > 21:
                self.can_player_move = False
                return False

            if player_turn == Move.STAND:
                self.can_player_move = False

            if player_turn == Move.DOUBLE_DOWN:
                self.can_player_move = False

        dealer_turn = dealer.take_turn(deck)
        if dealer.get_hand().get_total() > 21:
            return False
        if (
            player_turn == Move.STAND or player_turn == Move.DOUBLE_DOWN
        ) and dealer_turn == Move.STAND:
            return False
        return True

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

        self.deal(player, deck, dealer)

        while self.play_round(player, deck, dealer):
            # play round completes via side effects, therefore this loop condition is all we need
            pass

        dealer.reveal_hand()

        return self.evaluate(player.get_hand(), dealer.get_hand())

    def evaluate(self, player_hand, dealer_hand):
        """
        Blackjack scoring:
        In order of priority
            If the player busts, they always lose
            If the dealer busts the player wins
            If both players have 21, any natural 21 (no hits) wins
            If a tie, the result is a push
            Higher card wins
        :param player_hand:
        :param dealer_hand:
        :return:
        """

        if player_hand.get_total() > 21:
            return Result.DEFEAT
        elif dealer_hand.get_total() > 21:
            return Result.VICTORY
        elif player_hand.get_total() == 21 and dealer_hand.get_total() == 21:
            if player_hand.get_size() == 2 and dealer_hand.get_size() > 2:
                return Result.VICTORY
            elif player_hand.get_size() > 2 and dealer_hand.get_size() == 2:
                return Result.DEFEAT
            else:
                return Result.PUSH
        elif player_hand.get_total() == dealer_hand.get_total():
            return Result.PUSH
        else:
            return (
                Result.VICTORY
                if player_hand.get_total() > dealer_hand.get_total()
                else Result.DEFEAT
            )
