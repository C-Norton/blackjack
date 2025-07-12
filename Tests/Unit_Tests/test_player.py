"""
FILENAME: test_player.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import collections
from pathlib import Path

import pytest

import Blackjack
import Blackjack.main_menu
from Blackjack import player
from Blackjack.move import Move
from Blackjack.player import Player
from Blackjack.result import Result
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestPlayer:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        # TODO: Add your setup code here
        yield
        print(f"Tearing down class: {request.cls.__name__}")
        # TODO: Add your teardown code here

    @pytest.fixture
    def method_setup(self, request, mocker, generate_fake_card):
        print(f"Setting up method: {request.function.__name__}")
        self.fake_print = mocker.patch("builtins.print")
        self.fake_input = mocker.patch("builtins.input")
        self.fake_hand = mocker.Mock()
        self.deck = collections.deque()
        self.deck.append(generate_fake_card(Suit.CLUBS, Value.JACK))
        self.player = Player.from_name_bankroll("Player 1", 100)
        self.player.hand = self.fake_hand
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_player_creation(self, class_setup, method_setup):
        self.fake_input.side_effect = ["Player 1", "1000"]
        self.player = Blackjack.main_menu.new_player()
        assert type(self.player) is Player
        assert self.player.name == "Player 1"
        assert self.player.bankroll == 1000
        self.fake_print.reset_mock()
        assert self.fake_input.call_count == 2
        self.fake_input.reset_mock()

    def test_bad_input(self, class_setup, method_setup):
        path = Path("player 2.blackjack")
        self.fake_input.side_effect = ["Player 2", "Bad Input", "2000"]
        self.player = Blackjack.main_menu.new_player()
        assert type(self.player) is Player

        assert self.player.name == "Player 2"
        assert self.player.bankroll == 2000
        assert self.fake_input.call_count == 3
        Path.unlink(path)

    def test_update_bankroll(self, class_setup, method_setup):
        assert self.player.update_bankroll(100)
        assert self.player.bankroll == 200

    def test_negative_bankroll_update(self, class_setup, method_setup):
        assert self.player.update_bankroll(-100)
        assert self.player.bankroll == 0

    def test_invalid_bankroll_update(self, class_setup, method_setup):
        assert not self.player.update_bankroll(-101)

    def test_update_stats_victory(self, class_setup, method_setup):
        self.player.update_stats((Result.VICTORY, 100))
        assert self.player.stats.get("wins") == 1
        assert self.player.stats.get("bankroll") == 200

    def test_update_stats_defeat(self, class_setup, method_setup):
        self.player.update_stats((Result.DEFEAT, -100))
        assert self.player.stats.get("losses") == 1
        assert self.player.stats.get("bankroll") == 0

    def test_update_stats_push(self, class_setup, method_setup):
        self.player.update_stats((Result.PUSH, 100))
        assert self.player.stats.get("pushes") == 1
        assert self.player.stats.get("bankroll") == 100

    def test_update_stats_insufficient_funds(self, class_setup, method_setup):
        assert not self.player.update_stats((Result.DEFEAT, -101))

    # can't lose money on a victory
    def test_update_stats_invalid(self, class_setup, method_setup):
        assert not self.player.update_stats((Result.VICTORY, -100))

    def test_ante(self, class_setup, method_setup):
        self.fake_input.return_value = "100"
        self.player.ante()
        assert self.player.bet == 100

    def test_ante_invalid(self, class_setup, method_setup):
        self.fake_input.side_effect = ["hello", "101", "100"]
        self.player.ante()
        assert self.player.bet == 100

    def test_double_down(self, class_setup, method_setup):
        self.player.bet = 50
        assert self.player.double_down()

    def test_double_down_invalid(self, class_setup, method_setup):
        self.player.bet = 51
        assert not self.player.double_down()

    def test_take_turn_invalid(self, class_setup, method_setup):
        self.fake_input.side_effect = ["HOOT", "HIT"]
        assert self.player.take_turn(self.deck) == Move.HIT
        assert self.fake_input.call_count == 2

    def test_take_turn_HIT(self, class_setup, method_setup):
        self.fake_input.return_value = "HIT"
        assert self.player.take_turn(self.deck) == Move.HIT
        assert self.fake_input.call_count == 1
        assert len(self.deck) == 0

    def test_take_turn_STAND(self, class_setup, method_setup):
        self.fake_input.return_value = "STAND"
        assert self.player.take_turn(self.deck) == Move.STAND
        assert self.fake_input.call_count == 1
        assert len(self.deck) == 1

    def test_take_turn_DOUBLE_DOWN_valid(self, class_setup, method_setup):
        self.fake_input.return_value = "DOUBLE DOWN"
        assert self.player.take_turn(self.deck) == Move.DOUBLE_DOWN
        assert self.fake_input.call_count == 1
        assert len(self.deck) == 0

    def test_take_turn_DOUBLE_DOWN_invalid(self, class_setup, method_setup):
        self.fake_input.side_effect = ["DOUBLE DOWN", "hit"]
        self.player.hand = self.fake_hand
        self.player.bet = 51
        assert self.player.take_turn(self.deck) == Move.HIT
        assert self.fake_input.call_count == 2
        assert len(self.deck) == 0
        assert self.fake_hand.add_card.call_count == 1

    def test_save_load_player(self, class_setup, method_setup, mocker):
        path = Path("player 1.blackjack")
        try:
            my_player = Player("player 1", 1000)
            my_player.stats = {
                "name": "player 1",
                "bankroll": 1000,
                "wins": 5,
                "losses": 3,
                "pushes": 2,
            }
            player.save_player(my_player, path)
            assert path.exists()
            result = player.load_player(path)
            assert result == my_player

        except Exception as e:
            print(e)

        finally:
            Path.unlink(path)
