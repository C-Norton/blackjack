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
    deck: collections.deque[Card] = collections.deque()
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
        if dealer is None:
            dealer = Dealer()
        if deck is None:
            deck = generate_deck()
        self.deck: collections.deque[Card] = deck
        self.dealer: Dealer = dealer
        self.player: Player = player
        self._can_player_move: bool = True

    def _deal(self) -> None:
        """
        deal prepares the hand for play by dealing 2 cards to the player and 2 to dealer, alternating who gets what card
        it also requests an ante (initial bet) from the player

        Being a private method, this does not have to be implemented by the student, though it's implementation is
        suggested
        :return: None
        """
        self._can_player_move = True
        self.player.ante()
        if self.player.hand is None:
            self.player.hand = Hand()
        if self.dealer.hand is None:
            self.dealer.hand = Hand()
        self.player.deal_card(self.deck.pop())
        self.dealer.deal_card(self.deck.pop())
        self.player.deal_card(self.deck.pop())
        self.dealer.deal_card(self.deck.pop())

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
        if self._can_player_move:
            player_turn = self.player.take_turn(self.deck)
            if self.player.has_busted():
                self._can_player_move = False
                return False

            if player_turn == Move.STAND:
                self._can_player_move = False

            if player_turn == Move.DOUBLE_DOWN:
                self._can_player_move = False
        else:
            player_turn = Move.STAND
        dealer_turn = self.dealer.take_turn(self.deck)
        if self.dealer.has_busted():
            return False
        if (
            player_turn == Move.STAND or player_turn == Move.DOUBLE_DOWN
        ) and dealer_turn == Move.STAND:
            return False
        return True

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
            Update player
            Save stats
        :return:
        """
        self._deal()
        print("Dealer's Hand")
        print(str(self.dealer.hand))
        print(f"{self.player.name}'s Hand")
        print(str(self.player.hand))

        while self._play_round():
            print("Dealer's Hand")
            print(str(self.dealer.hand))
            print(f"{self.player.name}'s Hand")
            print(str(self.player.hand))
        print("Dealer's Hand after reveal")
        self.dealer.reveal_hand()
        print(f"{self.player.name}'s final hand")
        print(str(self.player.hand))
        result = self._evaluate()
        print(result.name)
        self.player.hand = None
        self.dealer.hand = None
        net_change: int = 0
        if result == Result.VICTORY:
            net_change = self.player.bet
        elif result == Result.DEFEAT:
            net_change = -self.player.bet
        else:
            net_change = 0
        return result, net_change

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
        player_hand:Optional [Hand] = self.player.hand
        dealer_hand: Optional [Hand] = self.dealer.hand
        if player_hand is None or dealer_hand is None:
            raise Exception("Hand is None")
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
