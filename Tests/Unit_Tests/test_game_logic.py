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
from Blackjack.suit import Suit
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
        self.fake_dealer_hand = mocker.Mock()
        self.fake_player_hand = mocker.Mock()
        self.fake_dealer = mocker.Mock()
        self.game = Blackjack.game.Game(self.fake_player,self.fake_dealer,self.deck)
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_generate_deck(self, class_setup, method_setup):
        # Generate deck
        deck = game.generate_deck()
        assert type(deck) is collections.deque
        assert len(deck) == 52
        assert type(deck.popleft()) is card.Card

    def test_play_round_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 22
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player.hand = self.fake_player_hand
        assert self.game._can_player_move
        assert not self.game.play_round()
        assert not self.game._can_player_move

    def test_play_round_hit(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 17
        assert self.game._can_player_move
        assert self.game.play_round()
        assert self.game._can_player_move

    def test_play_round_stand(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 17
        assert self.game._can_player_move
        assert self.game.play_round()
        assert not self.game._can_player_move

    def test_play_round_dealer_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 22
        assert self.game._can_player_move
        assert not self.game.play_round()
        assert self.game._can_player_move

    def test_play_round_double_down(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 16
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 22
        assert self.game._can_player_move
        assert not self.game.play_round()
        assert not self.game._can_player_move

    def test_deal(self, class_setup, method_setup, generate_fake_card, mocker):
        deck = collections.deque()
        fake_card_1 = generate_fake_card(Suit.SPADES, Value.ACE)
        fake_card_2 = generate_fake_card(Suit.CLUBS, Value.ACE)
        fake_card_3 = generate_fake_card(Suit.DIAMONDS, Value.ACE)
        fake_card_4 = generate_fake_card(Suit.HEARTS, Value.ACE)
        deck.append(fake_card_1)
        deck.append(fake_card_2)
        deck.append(fake_card_3)
        deck.append(fake_card_4)

        self.game.deal()
        assert self.fake_player.deal_card.call_count == 2
        assert self.fake_dealer.deal_card.call_count == 2
        assert self.game._can_player_move

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

    def test_game_bust(self, class_setup, method_setup, generate_fake_card, mocker):
        """
        This is a complicated test. This test unit needs to be broken down. Potentially by breaking new hand down into several functions


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
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player_hand.get_total.side_effect = [14, 24]
        fake_card1 = generate_fake_card(Suit.SPADES, Value.TEN)
        fake_card2 = generate_fake_card(Suit.SPADES, Value.SEVEN)
        fake_card3 = generate_fake_card(Suit.SPADES, Value.FOUR)
        fake_card4 = generate_fake_card(Suit.SPADES, Value.EIGHT)
        fake_card5 = generate_fake_card(Suit.SPADES, Value.JACK)
        self.deck.appendleft(fake_card1)
        self.deck.appendleft(fake_card2)
        self.deck.appendleft(fake_card3)
        self.deck.appendleft(fake_card4)
        self.deck.appendleft(fake_card5)

        fake_player_hand = mocker.Mock()
        fake_dealer_hand = mocker.Mock()
        fake_player_hand.get_total.side_effect = [14,24]
        fake_dealer_hand.get_total.return_value = 15

        self.fake_player.hand = fake_player_hand
        self.fake_dealer.hand = fake_dealer_hand

        self.fake_player.ante.return_value = 100

        result = self.game.new_hand()
        assert self.fake_player.deal_card.call_count == 2
        assert self.fake_dealer.deal_card.call_count == 2
        assert self.fake_player.take_turn.call_count == 1
        assert self.fake_dealer.take_turn.call_count == 0

        assert self.fake_player.ante.call_count == 1

        assert result == Result.DEFEAT

    def test_evaluate_player_wins(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.VICTORY


    def test_evaluate_player_blackjack_dealer_21(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 3
        self.fake_player_hand.get_size.return_value = 2
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()== Result.VICTORY


    def test_evaluate_player_21_dealer_blackjack(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.DEFEAT


    def test_evaluate_21_push(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 3
        self.fake_player_hand.get_size.return_value = 4
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()== Result.PUSH


    def test_evaluate_house_wins(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()== Result.DEFEAT


    def test_evaluate_push(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()== Result.PUSH


    def test_evaluate_player_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 24
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()==Result.DEFEAT


    def test_evaluate_dealer_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 24
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate()== Result.VICTORY


    def test_game_double_down(self, class_setup, method_setup):
        self.fake_input.side_effect = ["100", "Double"]
