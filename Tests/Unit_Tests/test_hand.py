"""
Channing
7/4/2025
Test for: hand.py
"""

import pytest

from Blackjack import hand
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestHand:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        yield
        print(f"Tearing down class: {request.cls.__name__}")
        # TODO: Add your teardown code here

    @pytest.fixture
    def method_setup(self, request, generate_fake_card):
        print(f"Setting up method: {request.function.__name__}")
        self.my_hand = hand.Hand()
        self.fake_card1 = generate_fake_card(Suit.CLUBS, Value.ACE)
        self.fake_card2 = generate_fake_card(Suit.SPADES, Value.QUEEN)
        self.fake_card3 = generate_fake_card(Suit.DIAMONDS, Value.ACE)
        self.fake_card4 = generate_fake_card(Suit.HEARTS, Value.SEVEN)
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_ace_progression(self, class_setup, method_setup):
        self.my_hand.add_card(self.fake_card1)
        assert self.my_hand.get_total() == 11
        assert self.my_hand.get_size() == 1

        self.my_hand.add_card(self.fake_card2)
        assert self.my_hand.get_total() == 21
        assert self.my_hand.get_size() == 2

        self.my_hand.add_card(self.fake_card3)
        assert self.my_hand.get_total() == 12
        assert self.my_hand.get_size() == 3

        self.my_hand.add_card(self.fake_card4)
        assert self.my_hand.get_total() == 19
        assert self.my_hand.get_size() == 4
        assert str(self.my_hand) == "7♥\nA♦\nQ♠\nA♣"
