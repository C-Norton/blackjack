"""
FILENAME: test_game_logic.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import collections

import pytest

import Blackjack
from Blackjack import card, game


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

    # todo: I added DI for the deck in new_hand. Update tests of main menu, and main menu itself, appropriately
    def test_game_logic_happy_path(self, class_setup, method_setup):
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
                Dealer hit: 5
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
