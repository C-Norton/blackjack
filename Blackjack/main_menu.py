"""
Main menu generates the menu system for the game.

It is implemented as a series of functions, rather than a class. It is also the main file for the application

The module's external interface shall consist of
main_menu() - displays the main menu, performs input validation and selects between three options, playing a new game,
creating a player, showing stats



"""

from pathlib import Path
from typing import Optional

from Blackjack.game import Game
from Blackjack.player import Player, load_player, save_player


def main_menu() -> None:
    """
    Option 1: Play new game, select player
    Option 2: Make a New Player
    Option 3: Check Stats
    """
    pass


def new_hand() -> None:
    """
    New hand runs a game of blackjack, and saves the players stats back to the player file
    :return: None
    """
    pass


def new_player() -> None:
    """
    new_player creates a new player. It handles the menu operations
    :return: the new player object
    """
    pass

def show_stats() -> None:
    """
    show stats shows the stats of an existing player based off playername
    :return: None
    """
    pass


if __name__ == "__main__":
    main_menu()
