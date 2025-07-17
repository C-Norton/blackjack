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
    while True:
        option: bool = None
        while not option:
            try:
                print("======= Welcome to BlackJack! =======")
                print("1. Play a new game")
                print("2. Create a new player")
                print("3. Check player stats")
                print("exit to leave")
                option = input("Please enter an option: ")
            except ValueError:
                print("Invalid input; please enter a number!")

        match option:
            case "1":
                print("Playing a hand")
                new_hand()
            case "2":
                print("Creating a player")
                new_player()
            case "3":
                print("Showing stats")
                show_stats()
            case "exit":
                return
            case _:
                print("Please enter a value between 1 and 3.")


def new_hand() -> None:
    """
    New hand runs a game of blackjack, and saves the players stats back to the player file
    :return: None
    """
    playername = input("What player will be playing?")
    path = Path(f"{playername.lower()}.blackjack")
    player = load_player(path)
    game = Game(player)
    player.update_stats(game.new_hand())
    save_player(player, path)


def new_player() -> None:
    """
    new_player creates a new player. It handles the menu operations
    :return: the new player object
    """
    print("======= New Player =======")
    name: str = input("Please enter player name: ")
    bankroll: Optional[int] = None
    while not bankroll:
        try:
            bankroll = int(input("Please enter starting bankroll: "))
        except ValueError:
            print("Invalid bankroll; please enter an integer")
    player = Player.from_name_bankroll(name, bankroll)
    save_player(player, Path(f"{name.lower()}.blackjack"))
    return player


def show_stats() -> None:
    """
    show stats shows the stats of an existing player based off playername
    :return: None
    """
    name = input("What player would you like to see stats for? ")
    player = load_player(Path(f"{name.lower()}.blackjack"))
    print(player.stats)


if __name__ == "__main__":
    main_menu()
