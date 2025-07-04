"""
FILENAME: test_game_logic.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import collections

import pytest

import Blackjack
from Blackjack import card


class TestGameLogic:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        # TODO: Add your setup code here
        yield
        print(f"Tearing down class: {request.cls.__name__}")
        # TODO: Add your teardown code here

    @pytest.fixture
    def method_setup(self, request):
        print(f"Setting up method: {request.function.__name__}")
        # TODO: Add your setup code here
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_generate_deck(self, class_setup, method_setup):
        # Generate deck
        deck = Blackjack.game.generate_deck()
        assert type(deck) is collections.deque
        assert len(deck) == 52
        assert type(deck.popleft()) is card.Card
