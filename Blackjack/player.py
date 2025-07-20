"""
Player represents the IO necessary to collect move information from the player,
as well as the hand management of the player.
"""

import collections
import json
from pathlib import Path
from typing import Optional

from .card import Card
from .game_participant import GameParticipant
from .hand import Hand
from .move import Move
from .result import Result


class OutOfMoneyException(Exception):
    def __init__(self, message: str):
        print(message)
        print("The house always wins!")


class Player(GameParticipant):
    def __init__(self, stats: dict):
        super().__init__()


    @classmethod
    def from_name_bankroll(cls, name: str, bankroll: int):
        """
        Create a new instance of the Player class using a name and bankroll.

        The method initializes a Player instance using the provided `name` and `bankroll`
        values and sets the default values for `wins`, `losses`, and `pushes` attributes
        to zero. This method is a convenience class method for easily creating a new
        Player object with basic attributes.

        Parameters:
            name: str
                The name of the player.
            bankroll: int
                The initial bankroll amount for the player.

        Returns:
            Player
                A new instance of the Player class initialized with the provided
                attributes.
        """
        pass

    def deal_card(self, card: Card):
        """
        Deal card gives a card to the player to add to the hand. As the player never flips cards face down, this is a
        simple one-liner to satisfy the game_participant abstract method
        """
        pass

    @property
    def bankroll(self) -> int:
        """Get the current bankroll amount from the stats dictionary."""
        pass

    @bankroll.setter
    def bankroll(self, new_amount: int) -> None:
        """Set the bankroll amount directly in the stats dictionary."""
        pass

    def update_stats(self, result_tuple: tuple) -> bool:
        """
        Updates player statistics and bankroll based on the result of a game round.

        This method processes the result of a game provided in the `result_tuple` and updates the player's
        win, loss, or push statistics accordingly. Additionally, it adjusts the player's bankroll based
        on the monetary outcome of the round.

        Parameters:
            result_tuple (tuple): A tuple containing the result of the game and its monetary outcome.
                                  The result is specified as an enumeration of type `Result`
                                  (e.g., Result.VICTORY, Result.PUSH), and the monetary outcome
                                  is a numeric value representing the gain or loss.

        Returns:
            bool: True if the stats and bankroll were successfully updated, False otherwise.
        """
        pass

    def ante(self) -> None:
        """
        Handles the ante process where the player must place a bet at the beginning of a game round.

        Summary:
        This function asks the player to place a bet (ante) and ensures that the bet is a valid
        integer within the player's available bankroll. If the bankroll is zero, an exception
        is raised. The betting process continues until the player inputs a valid value.

        Raises:
            OutOfMoneyException: Raised if the player's bankroll is zero when the function is called.

        Attributes:
            bet (int): Represents the amount the player wagers during the ante process. Must be
            set only after valid input from the player.

        """
        pass

    def double_down(self) -> bool:
        """
        Doubles the current bet if there are sufficient funds in the bankroll. The player will recieve exactly one
        additional card from the game.

        This method checks if the bet can be doubled without exceeding half of the bankroll,
        and if so, doubles the bet and returns True. Otherwise, it does not modify the bet
        and returns False.

        Returns:
            bool: True if the bet was successfully doubled, otherwise False.
        """
        pass

    def take_turn(self, deck: collections.deque) -> Move:
        """
        Prompts the player to take their turn in a card game and processes their chosen move.
        The player can select one of three moves: 'Hit', 'Stand', or 'Double Down'. Based on
        their choice, the method updates the state of the player's hand as well as processes
        the deck accordingly.

        Parameters:
            deck (collections.deque): The deck of cards used in the game, stored as a deque.

        Returns:
            Move: An enumeration indicating the move chosen by the player:
                   - Move.HIT: The player draws a card.
                   - Move.STAND: The player stands without drawing a card.
                   - Move.DOUBLE_DOWN: The player doubles their bet and draws one additional card.

        Raises:
            TypeError: If the deck is not a collections.deque.
        """
        pass

    def __eq__(self, other):
        """
        eq is a method that returns a boolean that determines if two objects are equal (not the same, equal)
        :param other: the item to compare against
        :return: true if equal 
        """
        pass


def load_player(path: Path) -> Player:
    """
    Load player is a module function that loads a player from a stats file. Note that hand is not created
    :param path: The path object representing the file to load from
    :return: a player object
    """
    pass


def save_player(
    player: Player,
    path: Path,
) -> None:
    """
    Save player is a module function that saves a player to a stats file. Note that hand is not saved.
    :param player: The player to save
    :param path: The filepath to save to
    """
    pass
