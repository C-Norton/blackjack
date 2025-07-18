"""
FILENAME: test_menu.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

from pathlib import Path

import pytest

import Blackjack
import Blackjack.main_menu
from Blackjack.player import Player


class TestMenu:
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
        self.fake_player = mocker.Mock()
        self.new_hand = mocker.patch(
            "Blackjack.game.Game.new_hand", return_value="mocked"
        )
        self.save_player = mocker.patch("Blackjack.main_menu.save_player")

        self.load_player = mocker.patch(
            "Blackjack.main_menu.load_player", return_value=self.fake_player
        )

        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_play_hand(self, class_setup, method_setup):
        self.fake_input.side_effect = ["1", "Player 1", "exit"]
        Blackjack.main_menu.main_menu()

        assert self.new_hand.call_count == 1
        assert self.save_player.call_count == 1

    def test_player_creation(self, class_setup, method_setup):
        self.fake_input.side_effect = ["Player 1", "1000"]
        self.player = Blackjack.main_menu.new_player()
        assert type(self.player) is Player
        assert self.player.name == "Player 1"
        assert self.player.bankroll == 1000
        self.fake_print.reset_mock()
        assert self.fake_input.call_count == 2
        self.fake_input.reset_mock()

    def test_bad_input(self, class_setup, method_setup, mocker):
        new_player = mocker.patch(
            "Blackjack.main_menu.new_player", return_value="mocked"
        )
        self.fake_input.side_effect = ["Foo", "2", "player 2", "1001", "exit"]
        Blackjack.main_menu.main_menu()

        assert new_player.call_count == 1

    def test_new_player(self, class_setup, method_setup):
        self.fake_input.side_effect = ["Player 1", "One Thousand", "1001"]
        new_player = Blackjack.main_menu.new_player()
        assert self.fake_input.call_count == 3
        assert new_player.name == "Player 1"
        assert new_player.bankroll == 1001

    def test_bad_input_player_creation(self, class_setup, method_setup):
        path = Path("player 2.blackjack")
        self.fake_input.side_effect = ["Player 2", "Bad Input", "2000"]
        self.player = Blackjack.main_menu.new_player()
        assert type(self.player) is Player

        assert self.player.name == "Player 2"
        assert self.player.bankroll == 2000
        assert self.fake_input.call_count == 3
        Path.unlink(path, missing_ok=True)
