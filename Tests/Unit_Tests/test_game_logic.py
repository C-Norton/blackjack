"""
FILENAME: test_game_logic.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import collections

import pytest

import Blackjack
from Blackjack import card, game
from Blackjack.move import Move
from Blackjack.result import Result
from Blackjack.value import Value


class TestGameLogic:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        # TODO: Add your setup code here
        yield
        print(f"Tearing down class: {request.cls.__name__}")
        # TODO: Add your teardown code here

    @pytest.fixture
    def method_setup(self, request, mocker):
        print(f"Setting up method: {request.function.__name__}")
        self.fake_input = mocker.patch("builtins.input")
        self.fake_print = mocker.patch("builtins.print")
        self.deck = collections.deque()
        self.fake_player = mocker.Mock()
        self.fake_player_hand = mocker.Mock()
        self.fake_dealer = mocker.Mock()
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_generate_deck(self, class_setup, method_setup):
        # Generate deck
        deck = Blackjack.game.generate_deck()
        assert type(deck) is collections.deque
        assert len(deck) == 52
        assert type(deck.popleft()) is card.Card

    def test_game_logic_invalid_inputs(self, class_setup, method_setup):
        """
        This function tests several full games.

        Game Scenarios:
            1:
                Player bankroll 100
                Player antes 150
                Result: Insufficient funds
            2:
                Player bankroll 100
                Player antes 100
                Dealer Cards: 7, 8
                Player cards: 10, 4
                Player Splits
                Result: Invalid Split
            3:
                Player bankroll 100
                Player antes 100
                Dealer Cards: 10, jack
                Player cards: ace, 8
                Player doubles down
                Result: Insufficient funds

        :param fake_print_fake_input:
        :return:
        """

    def test_game_bust(self, class_setup, method_setup, mocker):
        """

        Happy path should do the following

        accept an ante
        create a dealer
        deal 2 cards to dealer
        deal 2 cards to player
        Loop
            Accept a player move
            Accept a dealer move
        reveal
        resolve
        update player
        update stats
        This function tests several full games.

        Game Scenarios:
            1:
                Player bankroll 100
                Player antes 100
                Dealer Cards: 7, 8
                Player cards: 10, 4
                Player hit: Jack
                Result: Player Loss
            2:
                Player bankroll 200
                Player antes 100
                Dealer Cards: 10, jack
                Player cards: ace, 8
                Player doubles down
                Result: Player loss



        :param fake_print_fake_input:
        :return:
        """
        self.fake_input.side_effect = ["100", "Hit"]
        self.fake_player.get_bankroll.return_value = 100
        self.fake_player.get_move.side_effect = [Move.HIT, Move.HIT, Move.HIT]
        self.fake_dealer.get_move.return_value = [Move.HIT, Move.HIT]
        self.fake_player_hand.get_total.side_effect = [14, 24]
        fake_card1 = mocker.Mock()
        fake_card1.get_value.return_value = Value.TEN
        fake_card2 = mocker.Mock()
        fake_card2.get_value.return_value = Value.SEVEN
        fake_card3 = mocker.Mock()
        fake_card3.get_value.return_value = Value.FOUR
        fake_card4 = mocker.Mock()
        fake_card4.get_value.return_value = Value.EIGHT
        fake_card5 = mocker.Mock()
        fake_card5.get_value.return_value = Value.JACK
        self.deck.appendleft(fake_card1)
        self.deck.appendleft(fake_card2)
        self.deck.appendleft(fake_card3)
        self.deck.appendleft(fake_card4)
        self.deck.appendleft(fake_card5)
        assert self.fake_player.get_move.call_count == 3
        assert self.fake_dealer.call_count == 2
        assert self.fake_player.update_bankroll.call_count == 1
        assert self.fake_player.ante.call_count == 1
        assert game.new_hand(
            self.fake_player, deck=self.deck, dealer=self.fake_dealer
        ) == (Result.DEFEAT, -100)

    def test_game_double_down(self, class_setup, method_setup):
        self.fake_input.side_effect = ["100", "Double"]
