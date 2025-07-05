"""
FILENAME: test_stats.py

AUTHOR: Channing
CREATED ON: 7/4/2025

"""

import pytest
from Blackjack.stats import Stats


class test_stats:
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

    def test_win_loss(self, class_setup, method_setup):
        stats = Stats(1)
        assert Stats.get_wins() == 0
        assert Stats.get_losses() == 0
        assert Stats.get_bankroll() == 1
        stats.add_win()
        stats.adjust_bankroll(1)
        assert Stats.get_bankroll(2)
        stats.add_win()
        stats.adjust_bankroll(1)
        assert Stats.get_bankroll(3)
        stats.add_loss()
        stats.adjust_bankroll(-1)
        assert Stats.get_bankroll(2)
        assert Stats.get_wins() == 2
        assert Stats.get_losses() == 1

    def test_save(self):
        pass

    def test_load(self):
        pass
