"""
Game handles the flow of play, including running generating decks, running hands, and evaluating win/loss status

The external interface of game should consist of
Functions: generate_deck
Class Methods: Game.new_hand: plays a hand
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


def generate_deck() -> collections.deque:
    """
    generate deck generates a deck of 52 card objects, adds them to a deque, and shuffles them
    :return: the generated deque object
    """
    pass


class Game:
    """
    Game handles the flow of play, including generating new hands and all the helper methods therein
    """

    def __init__(
        self,
        player: Player,
        dealer: Optional[Dealer] = None,
        deck: Optional[collections.deque] = None,
    ):
        """
        __init__ creates a new Game instance, and sets up the class for play.

        :param player: the player object that will play in the game
        :param dealer: the dealer object that will play in the game
        """
        pass

    def _deal(self) -> None:
        """
        deal prepares the hand for play by dealing 2 cards to the player and 2 to dealer, alternating who gets what card
        it also requests an ante (initial bet) from the player

        Being a private method, this does not have to be implemented by the student, though it's implementation is
        suggested
        :return: None
        """
        pass

    def _play_round(self) -> bool:
        """
        _play_round returns a boolean as to if there should be another round
        Being a private method, this does not have to be implemented by the student, though it's implementation is
        suggested

        Note that tests exist for this method, as it was made private after the tests were written. Should you choose
        not to implement this, you can mark these tests using
        @pytest.mark.skip(reason="not implemented")
        in pytest to avoid running these irrelevant tests

        :return: boolean, true if another round is warranted
        """
        pass

    def new_hand(self) -> tuple[Result, int]:
        """
        Deals a new hand, plays the game, and returns a tuple of a result and the net change to bankroll
        Order of operations:
            player antes
            Deal cards to dealer
            Deal cards to player
            Until both players have STAND on all hands, or one player has busted:
                Accept Player move
                Accept dealer move
            Dealer reveals hidden card
            Resolve the hand
        :return:
        """
        pass

    def _evaluate(self) -> Result:
        """
        Blackjack scoring:
        In order of priority
            If the player busts, they always lose
            If the dealer busts the player wins
            If both players have 21, any natural 21 (no hits) wins
            If a tie, the result is a push
            Higher card wins

        Being a private method, this does not have to be implemented by the student, though it's implementation is
        suggested

        Note that tests exist for this method, as it was made private after the tests were written. Should you choose
        not to implement this, you can mark these tests using
        @pytest.mark.skip(reason="not implemented")
        in pytest to avoid running these irrelevant tests
        :return: a Result enum reflecting the result of the hand
        """
        pass
