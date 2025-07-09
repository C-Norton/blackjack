"""
FILENAME: test_dealer.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import collections

import pytest

from Blackjack import dealer
from Blackjack.move import Move
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestDealer:
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
        self.deck = collections.deque()
        self.fake_hand = mocker.Mock()
        self.my_dealer = dealer.Dealer(self.fake_hand)
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_blackjack(self, class_setup, method_setup, generate_fake_card):
        """
        In order to test this properly, we need to inject a mock hand instance into the dealer
        Hand 1 will have a deck like the below

        TOP OF DECK
        "A♣"
        "Q♠"
        "A♦"
        "7♥"
        BOTTOM OF DECK
        """
        fake_card1 = generate_fake_card(Suit.CLUBS, Value.ACE)
        fake_card2 = generate_fake_card(Suit.SPADES, Value.QUEEN)
        fake_card3 = generate_fake_card(Suit.DIAMONDS, Value.ACE)
        fake_card4 = generate_fake_card(Suit.HEARTS, Value.SEVEN)

        self.deck.append(fake_card1)
        self.deck.append(fake_card2)
        self.deck.append(fake_card3)
        self.deck.append(fake_card4)

        self.fake_hand.get_total.return_value = 0
        self.fake_hand.get_size.return_value = 0
        move1 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 3
        assert self.deck[0] == fake_card2
        assert move1 == Move.HIT

        self.fake_hand.get_total.return_value = 11
        self.fake_hand.get_size.return_value = 1
        move2 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 2
        assert self.deck[0] == fake_card3
        assert move2 == Move.HIT

        self.fake_hand.get_total.return_value = 21
        self.fake_hand.get_size.return_value = 2
        move3 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 2
        assert self.deck[0] == fake_card3
        assert move3 == Move.STAND

    def test_hit_stand_logic(self, class_setup, method_setup, generate_fake_card):
        """
        Hand 2 will have a deck like the below
        TOP OF DECK
        "5♣"
        "Q♠"
        "A♦"
        "7♥"
        BOTTOM OF DECK

        there will be no player or game class, of course, so the dealer will take each card in order


        Game 2 should be, Hit-Hit-Hit-Hit
                          (5) (15)(16)(23)
        """

        fake_card1 = generate_fake_card(Suit.CLUBS, Value.FIVE)
        fake_card2 = generate_fake_card(Suit.SPADES, Value.QUEEN)
        fake_card3 = generate_fake_card(Suit.DIAMONDS, Value.ACE)
        fake_card4 = generate_fake_card(Suit.HEARTS, Value.SEVEN)

        self.deck.append(fake_card1)
        self.deck.append(fake_card2)
        self.deck.append(fake_card3)
        self.deck.append(fake_card4)

        self.fake_hand.get_total.return_value = 0
        self.fake_hand.get_size.return_value = 0
        move1 = self.my_dealer.take_turn(self.deck)

        assert len(self.deck) == 3
        assert self.deck[0] == fake_card2
        assert move1 == Move.HIT

        self.fake_hand.get_total.return_value = 5
        self.fake_hand.get_size.return_value = 1
        move2 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 2
        assert self.deck[0] == fake_card3
        assert move2 == Move.HIT

        self.fake_hand.get_total.return_value = 15
        self.fake_hand.get_size.return_value = 2
        move3 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 1
        assert self.deck[0] == fake_card4
        assert move3 == Move.HIT

        self.fake_hand.get_total.return_value = 16
        self.fake_hand.get_size.return_value = 3
        move4 = self.my_dealer.take_turn(self.deck)
        assert len(self.deck) == 0
        assert move4 == Move.HIT

        self.fake_hand.get_total.return_value = 23
        self.fake_hand.get_size.return_value = 4
        move5 = self.my_dealer.take_turn(self.deck)
        assert move5 == Move.STAND
