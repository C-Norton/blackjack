""""""

from Blackjack.game import Game
from Blackjack.player import Player, load_player, save_player


def main_menu():
    """
    Option 1: Play new game, select player
    Option 2: Make a New Player
    Option 3: Check Stats
    """
    option = None
    while not option:
        try:
            print("======= Welcome to BlackJack! =======")
            print("1. Play a new game")
            print("2. Create a new player")
            print("3. Check player stats")
            option = int(input("Please enter an option: "))
        except ValueError:
            print("Invalid input; please enter a number!")

    match option:
        case 1:
            print("Playing a hand")
            Game.new_hand(Game(), Player("foo", 100))
        case 2:
            print("Creating a player")
            new_player()
        case 3:
            print("Showing stats")
            name = input("What player would you like to see stats for? ")
            player = load_player(name)
            print(player.stats)

        case _:
            print("Please enter a value between 1 and 3. Exiting")
            return


def new_player():
    print("======= New Player =======")
    name = input("Please enter player name: ")
    bankroll = None
    while not bankroll:
        try:
            bankroll = int(input("Please enter starting bankroll: "))
        except ValueError:
            print("Invalid bankroll; please enter an integer")
    player = Player(name, bankroll)
    save_player(player)
    return player


if __name__ == "__main__":
    main_menu()
