"""
FILENAME: test_player_edge_cases.py

AUTHOR: Enhanced Testing Suite
CREATED ON: 7/14/2025

Edge case and bad input tests for player.py module
"""

import collections

import pytest

from Blackjack.move import Move
from Blackjack.player import Player, OutOfMoneyException
from Blackjack.result import Result
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestPlayerEdgeCases:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        yield
        print(f"Tearing down class: {request.cls.__name__}")

    @pytest.fixture
    def method_setup(self, request, mocker, generate_fake_card):
        print(f"Setting up method: {request.function.__name__}")
        self.fake_print = mocker.patch("builtins.print")
        self.fake_input = mocker.patch("builtins.input")
        self.fake_hand = mocker.Mock()
        self.deck = collections.deque()
        self.deck.append(generate_fake_card(Suit.CLUBS, Value.JACK))
        self.player = Player.from_name_bankroll("Test Player", 100)
        self.player.hand = self.fake_hand
        yield
        print(f"Tearing down method: {request.function.__name__}")

    # ==================== ANTE EDGE CASES ====================

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",
            "abc",
            "-5",
            "0",
            "999999",
            "1.5",
            " ",
            "hit me",
            "!@#",
            "one hundred",
            "\n",
            "\t",
            "100.0",
            "-1",
            "0.5",
        ],
    )
    def test_ante_invalid_inputs_then_valid(
        self, invalid_input, class_setup, method_setup
    ):
        """Test that ante handles various invalid inputs before accepting valid input"""
        self.fake_input.side_effect = [invalid_input, "50"]
        self.player.ante()
        assert self.player.bet == 50
        assert self.fake_input.call_count == 2

    def test_ante_exceeds_bankroll_multiple_attempts(self, class_setup, method_setup):
        """Test ante with amounts exceeding bankroll, then valid amount"""
        self.fake_input.side_effect = ["150", "200", "999", "75"]
        self.player.ante()
        assert self.player.bet == 75

    def test_ante_exactly_bankroll(self, class_setup, method_setup):
        """Test ante with amount exactly equal to bankroll"""
        self.fake_input.return_value = "100"
        self.player.ante()
        assert self.player.bet == 100

    def test_ante_minimum_valid_amount(self, class_setup, method_setup):
        """Test ante with minimum valid amount (1)"""
        self.fake_input.return_value = "1"
        self.player.ante()
        assert self.player.bet == 1

    def test_ante_zero_bankroll_raises_exception(self, class_setup, method_setup):
        """Test that ante raises OutOfMoneyException when bankroll is 0"""
        self.player.stats["bankroll"] = 0
        with pytest.raises(OutOfMoneyException):
            self.player.ante()

    def test_ante_very_long_invalid_input_sequence(self, class_setup, method_setup):
        """Test resilience with many consecutive invalid inputs"""
        invalid_sequence = ["bad"] * 10 + ["50"]
        self.fake_input.side_effect = invalid_sequence
        self.player.ante()
        assert self.player.bet == 50
        assert self.fake_input.call_count == 11

    # ==================== MOVE INPUT EDGE CASES ====================

    @pytest.mark.parametrize(
        "move_input,expected_move",
        [
            ("HIT", Move.HIT),
            ("hit", Move.HIT),
            ("Hit", Move.HIT),
            ("  hit  ", Move.HIT),
            ("STAND", Move.STAND),
            ("stand", Move.STAND),
            ("Stand", Move.STAND),
            ("  STAND  ", Move.STAND),
            ("DOUBLE DOWN", Move.DOUBLE_DOWN),
            ("double down", Move.DOUBLE_DOWN),
            ("Double Down", Move.DOUBLE_DOWN),
            ("  double down  ", Move.DOUBLE_DOWN),
        ],
    )
    def test_take_turn_input_variations(
        self, move_input, expected_move, class_setup, method_setup
    ):
        """Test various valid input formats for moves"""
        self.fake_input.return_value = move_input
        result = self.player.take_turn(self.deck)
        assert result == expected_move

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",
            "xyz",
            "h",
            "s",
            "double",
            "down",
            "hit me",
            "please hit",
            "1",
            "0",
            "quit",
            "exit",
            "help",
            "?",
            "\n",
            "\t",
            "  ",
        ],
    )
    def test_take_turn_invalid_inputs_then_valid(
        self, invalid_input, class_setup, method_setup
    ):
        """Test take_turn with various invalid inputs followed by valid input"""
        self.fake_input.side_effect = [invalid_input, "hit"]
        result = self.player.take_turn(self.deck)
        assert result == Move.HIT
        assert self.fake_input.call_count == 2

    def test_take_turn_double_down_insufficient_funds_fallback(
        self, class_setup, method_setup
    ):
        """Test double down with insufficient funds falls back to asking again"""
        self.player.bet = 75  # More than half of 100 bankroll
        self.fake_input.side_effect = ["double down", "stand"]
        result = self.player.take_turn(self.deck)
        assert result == Move.STAND
        assert self.player.bet == 75  # Bet should not change

    def test_take_turn_double_down_exactly_half_bankroll(
        self, class_setup, method_setup
    ):
        """Test double down when bet is exactly half of bankroll"""
        self.player.bet = 50
        self.fake_input.return_value = "double down"
        result = self.player.take_turn(self.deck)
        assert result == Move.DOUBLE_DOWN
        assert self.player.bet == 100

    # ==================== BANKROLL EDGE CASES ====================

    def test_update_bankroll_exactly_zero_result(self, class_setup, method_setup):
        """Test bankroll update with exactly zero change"""
        initial_bankroll = self.player.bankroll
        self.player.bankroll += 0
        assert self.player.bankroll == initial_bankroll

    def test_update_bankroll_negative_exactly_bankroll(self, class_setup, method_setup):
        """Test bankroll update that would reduce to exactly zero"""
        self.player.bankroll -= 100
        assert self.player.bankroll == 0

    def test_update_bankroll_negative_exceeds_bankroll_by_one(
        self, class_setup, method_setup
    ):
        """Test bankroll update that exceeds bankroll by exactly one"""
        with pytest.raises(OutOfMoneyException):
            self.player.bankroll -= 101
        assert self.player.bankroll == 100  # Should remain unchanged

    def test_update_bankroll_very_large_positive(self, class_setup, method_setup):
        """Test bankroll update with very large positive amount"""
        self.player.bankroll += 999999
        assert self.player.bankroll == 1000099

    def test_bankroll_setter_negative_raises_error(self, class_setup, method_setup):
        """Test that setting negative bankroll raises ValueError"""
        with pytest.raises(OutOfMoneyException):
            self.player.bankroll = -1

    def test_bankroll_setter_zero_is_valid(self, class_setup, method_setup):
        """Test that setting bankroll to zero is valid"""
        self.player.bankroll = 0
        assert self.player.bankroll == 0

    # ==================== DOUBLE DOWN EDGE CASES ====================

    def test_double_down_exactly_half_bankroll(self, class_setup, method_setup):
        """Test double down when bet is exactly half of bankroll"""
        self.player.bet = 50
        assert self.player.double_down()
        assert self.player.bet == 100

    def test_double_down_one_over_half_bankroll(self, class_setup, method_setup):
        """Test double down when bet is one more than half of bankroll"""
        self.player.bet = 51
        assert not self.player.double_down()
        assert self.player.bet == 51  # Should remain unchanged

    def test_double_down_minimum_bet(self, class_setup, method_setup):
        """Test double down with minimum possible bet"""
        self.player.bet = 1
        assert self.player.double_down()
        assert self.player.bet == 2

    def test_double_down_with_odd_bankroll(self, class_setup, method_setup):
        """Test double down logic with odd bankroll amounts"""
        self.player.stats["bankroll"] = 101
        self.player.bet = 50  # Exactly half of 100, but bankroll is 101
        assert self.player.double_down()
        assert self.player.bet == 100

    # ==================== UPDATE STATS EDGE CASES ====================

    def test_update_stats_victory_zero_change(self, class_setup, method_setup):
        """Test victory with zero money change (edge case)"""
        initial_wins = self.player.stats.get("wins", 0)
        assert not self.player.update_stats((Result.VICTORY, 0))
        assert self.player.stats.get("wins") == initial_wins  # Should not increment

    def test_update_stats_victory_negative_change(self, class_setup, method_setup):
        """Test victory with negative money change (invalid scenario)"""
        initial_wins = self.player.stats.get("wins", 0)
        assert not self.player.update_stats((Result.VICTORY, -50))
        assert self.player.stats.get("wins") == initial_wins

    def test_update_stats_defeat_exactly_bankroll(self, class_setup, method_setup):
        """Test defeat that takes exactly all remaining money"""
        assert self.player.update_stats((Result.DEFEAT, -100))
        assert self.player.bankroll == 0
        assert self.player.stats.get("losses") == 1

    def test_update_stats_defeat_exceeds_bankroll(self, class_setup, method_setup):
        """Test defeat that would exceed bankroll"""
        initial_losses = self.player.stats.get("losses", 0)
        assert not self.player.update_stats((Result.DEFEAT, -101))
        assert self.player.bankroll == 100  # Should remain unchanged
        assert self.player.stats.get("losses") == initial_losses

    def test_update_stats_push_with_money_change(self, class_setup, method_setup):
        """Test push scenarios with various money changes"""
        initial_pushes = self.player.stats.get("pushes", 0)
        assert self.player.update_stats((Result.PUSH, 100))
        assert self.player.stats.get("pushes") == initial_pushes + 1
        assert self.player.bankroll == 100  # Push shouldn't change bankroll

    # ==================== PLAYER CREATION EDGE CASES ====================

    def test_from_name_bankroll_zero_bankroll(self, class_setup, method_setup):
        """Test creating player with zero bankroll"""
        player = Player.from_name_bankroll("Broke Player", 0)
        assert player.bankroll == 0
        assert player.name == "Broke Player"

    def test_from_name_bankroll_very_large_bankroll(self, class_setup, method_setup):
        """Test creating player with very large bankroll"""
        player = Player.from_name_bankroll("Rich Player", 999999999)
        assert player.bankroll == 999999999

    def test_from_name_bankroll_empty_name(self, class_setup, method_setup):
        """Test creating player with empty name"""
        player = Player.from_name_bankroll("", 100)
        assert player.name == ""
        assert player.bankroll == 100

    def test_from_name_bankroll_special_characters_name(
        self, class_setup, method_setup
    ):
        """Test creating player with special characters in name"""
        special_name = "Player!@#$%^&*()_+-=[]{}|;:,.<>?"
        player = Player.from_name_bankroll(special_name, 100)
        assert player.name == special_name

    # ==================== EQUALITY EDGE CASES ====================

    def test_player_equality_identical_stats(self, class_setup, method_setup):
        """Test player equality with identical stats"""
        player1 = Player.from_name_bankroll("Test", 100)
        player2 = Player.from_name_bankroll("Test", 100)
        assert player1 == player2

    def test_player_equality_different_bet_same_stats(self, class_setup, method_setup):
        """Test that players are equal even with different current bets"""
        player1 = Player.from_name_bankroll("Test", 100)
        player2 = Player.from_name_bankroll("Test", 100)
        player1.bet = 50
        player2.bet = 75
        assert player1 == player2  # Bet is not part of stats

    def test_player_equality_different_bankroll(self, class_setup, method_setup):
        """Test player inequality with different bankrolls"""
        player1 = Player.from_name_bankroll("Test", 100)
        player2 = Player.from_name_bankroll("Test", 200)
        assert player1 != player2
