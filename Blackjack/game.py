"""
Game handles the flow of play
"""

import collections
import random

from .card import Card
from .player import Player
from .dealer import Dealer
from .suit import Suit
from .value import Value


def new_hand(player, deck):
    """
    Deals a new hand, plays the game, and returns a tuple of a result and the net change to bankroll
    Order of operations:
        player antes
        Deal cards to dealer
        Deal cards to player
        Until both players have STAND on all hands:
            Accept Player move
            Accept dealer move
        Dealer reveals hidden card
        Resolve the hand
        Update player
        Save stats
    :return:
    """
    deck = generate_deck()
    dealer = Dealer()


def new_player():
    print("======= New Player =======")
    name = input("Please enter player name: ")
    bankroll = None
    while not bankroll:
        try:
            bankroll = int(input("Please enter starting bankroll: "))
        except ValueError:
            print("Invalid bankroll; please enter an integer")
    return Player(name, bankroll)


def load_player(playername):
    return Player()


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
            new_hand()
        case 2:
            print("Creating a player")
            new_player()
        case 3:
            print("Showing stats")
            name = input("What player would you like to see stats for? ")
            player = load_player(name)
            print(player.get_stats())

        case default:
            print("Please enter a value between 1 and 3. Exiting")
            return


def generate_deck():
    deck = collections.deque()
    for suit in Suit:
        for value in Value:
            card = Card(suit, value)
            deck.append(card)
    random.shuffle(deck)
    return deck
