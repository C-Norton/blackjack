""""""
from pathlib import Path

from Blackjack.game import Game
from Blackjack.player import Player, load_player, save_player


def main_menu():
    """
    Option 1: Play new game, select player
    Option 2: Make a New Player
    Option 3: Check Stats
    """
    while True:
        option = None
        while not option:
            try:
                print("======= Welcome to BlackJack! =======")
                print("1. Play a new game")
                print("2. Create a new player")
                print("3. Check player stats")
                print("exit to leave")
                option = int(input("Please enter an option: "))
            except ValueError:
                print("Invalid input; please enter a number!")

        match option:
            case 1:
                print("Playing a hand")
                playername = input("What player will be playing?")
                player = load_player(Path(f"{playername.lower()}.blackjack"))
                game = Game(player)
                game.new_hand()
            case 2:
                print("Creating a player")
                new_player()
            case 3:
                print("Showing stats")
                name = input("What player would you like to see stats for? ")
                player = load_player(Path(f"{name.lower()}.blackjack"))
                print(player.stats)
                
            case "exit":
                return
            case _:
                print("Please enter a value between 1 and 3.")


def new_player():
    """
    new_player creates a new player. It handles the menu operations
    :return: the new player object
    """
    print("======= New Player =======")
    name = input("Please enter player name: ")
    bankroll = None
    while not bankroll:
        try:
            bankroll = int(input("Please enter starting bankroll: "))
        except ValueError:
            print("Invalid bankroll; please enter an integer")
    player = Player.from_name_bankroll(name, bankroll)
    save_player(player,Path(f"{name.lower()}.blackjack"))
    return player


if __name__ == "__main__":
    main_menu()
