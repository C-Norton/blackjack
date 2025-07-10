"""
Game handles the flow of play
"""

import collections
import random
from typing import Optional

from .card import Card
from .dealer import Dealer
from .hand import Hand
from .move import Move
from .player import Player
from .result import Result
from .suit import Suit
from .value import Value


def generate_deck()->collections.deque:
    """
    generate deck generates a deck of 52 card objects, adds them to a deque, and shuffles them
    :return: the generated deque object
    """
    deck :collections.deque[Card] = collections.deque()
    for suit in Suit:
        for value in Value:
            card = Card(suit, value)
            deck.append(card)
    random.shuffle(deck)
    return deck


class Game:
    """
    Game handles the flow of play, including generating new hands and all the helper methods therein
    """
    def __init__(self, player:Player, dealer:Optional[Dealer]=None, deck:Optional[collections.deque]=None):
        """
        __init__ creates a new Game instance, and sets up the class for play.

        :param player: the player object that will play in the game
        :param dealer: the dealer object that will play in the game
        """
        if dealer is None:
            dealer = Dealer()
        if deck is None:
            deck = generate_deck()
        self.deck = deck
        self.dealer = dealer
        self.player = player
        self._can_player_move = True



    def deal(self)->None:
        """
        deal prepares the hand for play by dealing 2 cards to the player and 2 to dealer, alternating who gets what card
        it also requests an ante (initial bet) from the player
        :return: None
        """
        self._can_player_move = True
        self.player.ante()
        self.dealer.hand = Hand()
        self.player.hand = Hand()
        self.player.deal_card(self.deck)
        self.dealer.deal_card(self.deck)
        self.player.deal_card(self.deck)
        self.dealer.deal_card(self.deck)

    def play_round(self)->bool:
        """
        play round returns a boolean as to if there should be another round
        :return: boolean, true if another round is warranted
        """
        print("Dealer's Hand")
        print(str(self.dealer.hand))
        print(f"{self.player.name}'s Hand")
        print(str(self.player.hand))
        if self._can_player_move:
            player_turn = self.player.take_turn(self.deck)
            if self.player.hand.get_total() > 21:
                self._can_player_move = False
                return False

            if player_turn == Move.STAND:
                self._can_player_move = False

            if player_turn == Move.DOUBLE_DOWN:
                self._can_player_move = False
        else:
            player_turn = Move.STAND
        dealer_turn = self.dealer.take_turn(self.deck)
        if self.dealer.hand.get_total() > 21:
            return False
        if (
            player_turn == Move.STAND or player_turn == Move.DOUBLE_DOWN
        ) and dealer_turn == Move.STAND:
            return False
        return True

    def new_hand(self)->Result:
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
        self.deal()

        while self.play_round():
            # play round completes via side effects, therefore this loop condition is all we need
            pass

        self.dealer.reveal_hand()

        return self.evaluate()

    def evaluate(self)->Result:
        """
        Blackjack scoring:
        In order of priority
            If the player busts, they always lose
            If the dealer busts the player wins
            If both players have 21, any natural 21 (no hits) wins
            If a tie, the result is a push
            Higher card wins
        :return: a Result enum reflecting the result of the hand
        """
        player_hand = self.player.hand
        dealer_hand = self.dealer.hand
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
