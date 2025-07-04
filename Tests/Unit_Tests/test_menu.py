"""
FILENAME: test_menu.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import pytest

import Blackjack
from Blackjack import player


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
        self.new_hand = mocker.patch("Blackjack.game.new_hand", return_value="mocked")
        self.new_player = mocker.patch(
            "Blackjack.game.new_player", return_value="mocked"
        )
        self.load_player = mocker.patch(
            "Blackjack.game.load_player", return_value="mocked"
        )

        yield
        print(f"Tearing down method: {request.function.__name__}")
        # TODO: Add your teardown code here

    def test_play_hand(self, class_setup, method_setup):

        self.fake_input.side_effect = ["1"]
        Blackjack.game.main_menu()

        assert self.fake_print.call_count == 5
        assert self.fake_input.call_count == 1
        assert self.new_hand.call_count == 1

    def test_bad_input(self, class_setup, method_setup):
        self.fake_input.side_effect = ["Foo", 2]
        Blackjack.game.main_menu()

        assert self.new_player.call_count == 1

        assert self.fake_print.call_count == 10
        assert self.fake_input.call_count == 2

        self.fake_print.reset_mock()
        self.fake_input.reset_mock()
        self.load_player.return_value = player.Player("Player 1", 1000)
        self.fake_input.side_effect = ["3", "Player 1"]
        Blackjack.game.main_menu()
        assert self.fake_print.call_count == 6
        assert self.fake_input.call_count == 2
        assert self.load_player.call_count == 1
