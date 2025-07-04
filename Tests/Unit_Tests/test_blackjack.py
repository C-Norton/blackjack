import collections

import pytest
from Blackjack import player
from Blackjack.player import Player
import Blackjack.game


def test_game_logic_invalid_inputs(mocker):
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
    fake_input = mocker.patch("builtins.input")
    fake_print = mocker.patch("builtins.print")


# todo: I added DI for the deck in new_hand. Update tests of main menu, and main menu itself, appropriately
def test_game_logic_happy_path(mocker):
    """

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
            Dealer hit: 5
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
    fake_input = mocker.patch("builtins.input")
    fake_print = mocker.patch("builtins.print")
    deck = collections.deque()
