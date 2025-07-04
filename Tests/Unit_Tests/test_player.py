"""
FILENAME: test_player.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import pytest
import Blackjack
from Blackjack.player import Player


class TestPlayer:
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
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_player_creation(self, class_setup, method_setup):

        self.fake_input.side_effect = ["Player 1", "1000"]
        self.player = Blackjack.game.new_player()
        assert type(self.player) is Player
        assert self.player.get_name() == "Player 1"
        assert self.player.get_bankroll() == 1000
        assert type(self.player.get_stats()) is dict
        assert self.fake_input.call_count == 2
        self.fake_input.reset_mock()

    def test_bad_input(self, class_setup, method_setup):
        self.fake_input.side_effect = ["Player 2", "Bad Input", "2000"]
        self.player = Blackjack.game.new_player()
        assert type(self.player) is Player

        assert self.player.get_name() == "Player 2"
        assert self.player.get_bankroll() == 2000
        assert type(self.player.get_stats()) is dict
        assert self.fake_input.call_count == 3
