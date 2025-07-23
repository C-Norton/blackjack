"""
FILENAME: test_game.py

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
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_player.hand = self.fake_player_hand
        self.game = Blackjack.game.Game(self.fake_player, self.fake_dealer, self.deck)
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
        assert not self.game._play_round()
        assert not self.game._can_player_move

    def test_play_round_hit(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 17
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False
        assert self.game._can_player_move
        assert self.game._play_round()
        assert self.game._can_player_move

    def test_play_round_stand(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 17
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False
        assert self.game._can_player_move
        assert self.game._play_round()
        assert not self.game._can_player_move

    def test_play_round_dealer_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 22
        self.fake_player.has_busted.return_value = True
        self.fake_player.has_busted.return_value = False
        assert self.game._can_player_move
        assert not self.game._play_round()
        assert self.game._can_player_move

    def test_play_round_double_down(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 16
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_player.hand = self.fake_player_hand
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_dealer_hand.get_total.return_value = 22
        assert self.game._can_player_move
        assert not self.game._play_round()
        assert not self.game._can_player_move

    def test_deal(self, class_setup, method_setup, generate_fake_card):
        fake_card_1 = generate_fake_card(Suit.SPADES, Value.ACE)
        fake_card_2 = generate_fake_card(Suit.CLUBS, Value.ACE)
        fake_card_3 = generate_fake_card(Suit.DIAMONDS, Value.ACE)
        fake_card_4 = generate_fake_card(Suit.HEARTS, Value.ACE)
        self.deck.append(fake_card_1)
        self.deck.append(fake_card_2)
        self.deck.append(fake_card_3)
        self.deck.append(fake_card_4)

        self.game._deal()
        assert self.fake_player.deal_card.call_count == 2
        assert self.fake_dealer.deal_card.call_count == 2
        assert self.game._can_player_move

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


        :param fake_print_fake_input:
        :return:
        """
        self.fake_input.side_effect = ["100", "Hit"]
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player_hand.get_total.return_value = 24
        self.fake_dealer_hand.get_total.return_value = 15
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

        self.fake_player.ante.return_value = 100
        self.fake_player.bet = 100
        result = self.game.new_hand()
        assert self.fake_player.deal_card.call_count == 2
        assert self.fake_dealer.deal_card.call_count == 2
        assert self.fake_player.take_turn.call_count == 1
        assert self.fake_dealer.take_turn.call_count == 0

        assert self.fake_player.ante.call_count == 1

        assert result == (Result.DEFEAT, -100)

    def test_evaluate_player_wins(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.VICTORY

    def test_evaluate_player_blackjack_dealer_21(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 3
        self.fake_player_hand.get_size.return_value = 2
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.VICTORY

    def test_evaluate_player_21_dealer_blackjack(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.DEFEAT

    def test_evaluate_21_push(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 3
        self.fake_player_hand.get_size.return_value = 4
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.PUSH

    def test_evaluate_house_wins(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.DEFEAT

    def test_evaluate_push(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.PUSH

    def test_evaluate_player_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 24
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.DEFEAT

    def test_evaluate_dealer_bust(self, class_setup, method_setup):
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 24
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game._evaluate() == Result.VICTORY

    def test_game_double_down(self, class_setup, method_setup):
        self.fake_input.side_effect = ["100", "Double"]
    def test_game_player_bust(self, class_setup, method_setup, generate_fake_card, mocker):
        """Player busts - dealer wins regardless of dealer total"""
        self.fake_input.side_effect = ["100", "Hit"]
        self.fake_player.take_turn.return_value = Move.HIT
        self.fake_player_hand.get_total.return_value = 22  # Player busts
        self.fake_dealer_hand.get_total.return_value = 15  # Dealer total irrelevant

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),   # Player card 1
            generate_fake_card(Suit.HEARTS, Value.SEVEN), # Dealer card 1
            generate_fake_card(Suit.CLUBS, Value.FOUR),   # Player card 2
            generate_fake_card(Suit.DIAMONDS, Value.EIGHT), # Dealer card 2
            generate_fake_card(Suit.SPADES, Value.JACK),  # Player hit card
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 100
        self.fake_player.bet = 100
        result = self.game.new_hand()

        assert result == (Result.DEFEAT, -100)

    def test_game_dealer_bust(self, class_setup, method_setup, generate_fake_card):
        """Dealer busts - player wins regardless of player total"""
        self.fake_input.side_effect = ["50"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.side_effect = [Move.HIT, Move.HIT, Move.STAND]
        self.fake_player_hand.get_total.return_value = 18  # Player total
        self.fake_dealer_hand.get_total.return_value = 23  # Dealer busts

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.SEVEN),
            generate_fake_card(Suit.CLUBS, Value.EIGHT),
            generate_fake_card(Suit.DIAMONDS, Value.EIGHT),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 50
        self.fake_player.bet = 50
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = True

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 50)

    def test_game_player_blackjack_vs_dealer_21(self, class_setup, method_setup, generate_fake_card):
        """Player blackjack beats dealer 21 (3+ cards)"""
        self.fake_input.side_effect = ["75"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 2  # Blackjack
        self.fake_dealer_hand.get_size.return_value = 3  # 21 with 3 cards

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.ACE),
            generate_fake_card(Suit.HEARTS, Value.SEVEN),
            generate_fake_card(Suit.CLUBS, Value.KING),
            generate_fake_card(Suit.DIAMONDS, Value.FOUR),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 75
        self.fake_player.bet = 75
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 75)

    def test_game_dealer_blackjack_vs_player_21(self, class_setup, method_setup, generate_fake_card):
        """Dealer blackjack beats player 21 (3+ cards)"""
        self.fake_input.side_effect = ["60"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 3  # 21 with 3 cards
        self.fake_dealer_hand.get_size.return_value = 2  # Blackjack

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.SEVEN),
            generate_fake_card(Suit.HEARTS, Value.ACE),
            generate_fake_card(Suit.CLUBS, Value.SEVEN),
            generate_fake_card(Suit.DIAMONDS, Value.KING),
            generate_fake_card(Suit.SPADES, Value.SEVEN),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 60
        self.fake_player.bet = 60
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.DEFEAT, -60)

    def test_game_both_blackjack_push(self, class_setup, method_setup, generate_fake_card):
        """Both player and dealer have blackjack - push"""
        self.fake_input.side_effect = ["80"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 2  # Blackjack
        self.fake_dealer_hand.get_size.return_value = 2  # Blackjack

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.ACE),
            generate_fake_card(Suit.HEARTS, Value.ACE),
            generate_fake_card(Suit.CLUBS, Value.KING),
            generate_fake_card(Suit.DIAMONDS, Value.QUEEN),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 80
        self.fake_player.bet = 80
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.PUSH, 0)

    def test_game_player_wins_higher_total(self, class_setup, method_setup, generate_fake_card):
        """Player wins with higher total (no blackjack)"""
        self.fake_input.side_effect = ["40"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 19
        self.fake_player_hand.get_size.return_value = 3
        self.fake_dealer_hand.get_size.return_value = 3

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.NINE),
            generate_fake_card(Suit.CLUBS, Value.FIVE),
            generate_fake_card(Suit.DIAMONDS, Value.FIVE),
            generate_fake_card(Suit.SPADES, Value.FIVE),
            generate_fake_card(Suit.HEARTS, Value.FIVE),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 40
        self.fake_player.bet = 40
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 40)

    def test_game_dealer_wins_higher_total(self, class_setup, method_setup, generate_fake_card):
        """Dealer wins with higher total (no blackjack)"""
        self.fake_input.side_effect = ["35"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 18
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 3

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.EIGHT),
            generate_fake_card(Suit.DIAMONDS, Value.FIVE),
            generate_fake_card(Suit.SPADES, Value.FIVE),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 35
        self.fake_player.bet = 35
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.DEFEAT, -35)

    def test_game_push_same_totals(self, class_setup, method_setup, generate_fake_card):
        """Push - same totals (not 21)"""
        self.fake_input.side_effect = ["25"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 19
        self.fake_dealer_hand.get_total.return_value = 19
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 3

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.NINE),
            generate_fake_card(Suit.DIAMONDS, Value.FOUR),
            generate_fake_card(Suit.SPADES, Value.FIVE),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 25
        self.fake_player.bet = 25
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.PUSH, 0)

    def test_game_push_both_21_non_blackjack(self, class_setup, method_setup, generate_fake_card):
        """Push - both have 21 but neither is blackjack"""
        self.fake_input.side_effect = ["90"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 3  # Not blackjack
        self.fake_dealer_hand.get_size.return_value = 4  # Not blackjack

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.SEVEN),
            generate_fake_card(Suit.HEARTS, Value.SEVEN),
            generate_fake_card(Suit.CLUBS, Value.SEVEN),
            generate_fake_card(Suit.DIAMONDS, Value.SEVEN),
            generate_fake_card(Suit.SPADES, Value.SEVEN),
            generate_fake_card(Suit.HEARTS, Value.SEVEN),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 90
        self.fake_player.bet = 90
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.PUSH, 0)

    def test_game_double_down_win(self, class_setup, method_setup, generate_fake_card):
        """Player doubles down and wins"""
        self.fake_input.side_effect = ["30"]
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 19
        self.fake_player_hand.get_size.return_value = 3
        self.fake_dealer_hand.get_size.return_value = 2

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.FIVE),
            generate_fake_card(Suit.DIAMONDS, Value.NINE),
            generate_fake_card(Suit.SPADES, Value.FIVE),  # Double down card
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 30
        self.fake_player.bet = 60  # Doubled
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 60)

    def test_game_double_down_lose(self, class_setup, method_setup, generate_fake_card):
        """Player doubles down and loses"""
        self.fake_input.side_effect = ["45"]
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 18
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_player_hand.get_size.return_value = 3
        self.fake_dealer_hand.get_size.return_value = 2

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.FIVE),
            generate_fake_card(Suit.DIAMONDS, Value.TEN),
            generate_fake_card(Suit.SPADES, Value.THREE),  # Double down card
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 45
        self.fake_player.bet = 90  # Doubled
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.DEFEAT, -90)

    def test_game_double_down_bust(self, class_setup, method_setup, generate_fake_card):
        """Player doubles down and busts"""
        self.fake_input.side_effect = ["20"]
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_player_hand.get_total.return_value = 25  # Bust
        self.fake_dealer_hand.get_total.return_value = 18  # Irrelevant
        self.fake_player_hand.get_size.return_value = 3
        self.fake_dealer_hand.get_size.return_value = 2

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.EIGHT),
            generate_fake_card(Suit.CLUBS, Value.TEN),
            generate_fake_card(Suit.DIAMONDS, Value.TEN),
            generate_fake_card(Suit.SPADES, Value.FIVE),  # Double down card causing bust
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 20
        self.fake_player.bet = 40  # Doubled
        self.fake_player.has_busted.return_value = True
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.DEFEAT, -40)

    def test_game_minimum_totals(self, class_setup, method_setup, generate_fake_card):
        """Edge case: Minimum possible winning scenario"""
        self.fake_input.side_effect = ["15"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 17
        self.fake_dealer_hand.get_total.return_value = 16
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.SEVEN),
            generate_fake_card(Suit.DIAMONDS, Value.SIX),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 15
        self.fake_player.bet = 15
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 15)

    def test_game_maximum_non_bust_totals(self, class_setup, method_setup, generate_fake_card):
        """Edge case: Maximum totals without busting"""
        self.fake_input.side_effect = ["10"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 20
        self.fake_player_hand.get_size.return_value = 4
        self.fake_dealer_hand.get_size.return_value = 4

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.FIVE),
            generate_fake_card(Suit.HEARTS, Value.FIVE),
            generate_fake_card(Suit.CLUBS, Value.FIVE),
            generate_fake_card(Suit.DIAMONDS, Value.FIVE),
            generate_fake_card(Suit.SPADES, Value.SIX),
            generate_fake_card(Suit.HEARTS, Value.FIVE),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 10
        self.fake_player.bet = 10
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.VICTORY, 10)

    def test_game_dealer_exactly_17_boundary(self, class_setup, method_setup, generate_fake_card):
        """Edge case: Dealer at exactly 17 (should stand)"""
        self.fake_input.side_effect = ["55"]
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player_hand.get_total.return_value = 16
        self.fake_dealer_hand.get_total.return_value = 17  # Dealer stands on 17
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2

        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.TEN),
            generate_fake_card(Suit.HEARTS, Value.TEN),
            generate_fake_card(Suit.CLUBS, Value.SIX),
            generate_fake_card(Suit.DIAMONDS, Value.SEVEN),
        ]
        for card in reversed(fake_cards):
            self.deck.appendleft(card)

        self.fake_player.ante.return_value = 55
        self.fake_player.bet = 55
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.new_hand()
        assert result == (Result.DEFEAT, -55)