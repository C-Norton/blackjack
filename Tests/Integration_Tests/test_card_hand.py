"""
FILENAME: test_card_hand.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import pytest

from Blackjack import hand, card
from Blackjack.suit import Suit
from Blackjack.value import Value


class Testtest_card_hand:
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
        self.my_hand = hand.Hand()
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_hand_flip_str(self, class_setup, method_setup):
        card1 = card.Card(Suit.SPADES, Value.SEVEN)
        card2 = card.Card(Suit.CLUBS, Value.TEN)
        card1.flip()
        self.my_hand.add_card(card1)
        self.my_hand.add_card(card2)
        assert str(self.my_hand) == "10♣\n##"
