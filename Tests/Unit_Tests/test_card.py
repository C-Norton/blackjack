"""
FILENAME: test_card.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import pytest

from Blackjack import card
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestCard:
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

    def test_cards(self, class_setup, method_setup, mocker):
        card1 = card.Card(Suit.SPADES, Value.SEVEN)
        card2 = card.Card(Suit.CLUBS, Value.TEN)
        card3 = card.Card(Suit.DIAMONDS, Value.KING)
        card4 = card.Card(Suit.HEARTS, Value.ACE)

        # Stupid checks, but hey, just to be sure
        assert card1.value == Value.SEVEN
        assert card1.suit == Suit.SPADES
        assert card2.value == Value.TEN
        assert card2.suit == Suit.CLUBS
        assert card3.value == Value.KING
        assert card3.suit == Suit.DIAMONDS
        assert card4.value == Value.ACE
        assert card4.suit == Suit.HEARTS

        assert str(card1) == "7♠"
        assert str(card2) == "10♣"
        assert str(card3) == "K♦"
        assert str(card4) == "A♥"

        # The checks in this block are redundant, but this verifies
        # That the representation comes from __str__ and not __repr__
        assert card1.__str__() == "7♠"
        assert card2.__str__() == "10♣"
        assert card3.__str__() == "K♦"
        assert card4.__str__() == "A♥"

        card1.face_down = True
        assert card1.face_down
        assert card1.__str__() == "##"
        assert str(card1) == "##"
        card1.face_down = False
        assert card1.__str__() == "7♠"
        assert str(card1) == "7♠"
