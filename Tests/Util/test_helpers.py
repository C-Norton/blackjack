# test_helpers.py
import collections

import pytest


@pytest.fixture
def generate_fake_card(mocker):
    def g(fake_suit, fake_value):
        m = mocker.Mock()
        m.get_suit.return_value = fake_suit
        m.get_value.return_value = fake_value
        m.__str__ = mocker.Mock(return_value=str(fake_value) + str(fake_suit))
        return m

    return g


def generate_fake_stats(mocker):
    def g(bankroll=100, wins=0, losses=0, pushes=0):
        m = mocker.Mock()
        m.get_wins.return_value = wins
        m.get_losses.return_value = losses
        m.get_pushes.return_value = pushes
        m.get_bankroll.return_value = bankroll
        m.add_win = mocker.Mock()
        m.add_loss = mocker.Mock()
        m.add_push = mocker.Mock()
        m.adjust_bankroll = mocker.Mock()
        m.save = mocker.Mock()
        m.load = mocker.Mock()
        return m
