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
        self.name: str = stats["name"]
        self.stats: dict = stats
        self.bet: int = 0
        self.hand: Optional[Hand] = None

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
        return Player({"name": name, "bankroll": bankroll, "wins": 0, "losses": 0, "pushes": 0, })

    def deal_card(self, card: Card):
        """
        Deal card gives a card to the player to add to the hand. As the player never flips cards face down, this is a
        simple one-liner to satisfy the game_participant abstract method
        """
        self.hand.add_card(card)



    @property
    def bankroll(self) -> int:
        """Get the current bankroll amount from the stats dictionary."""
        return self.stats["bankroll"]

    @bankroll.setter
    def bankroll(self, new_amount: int) -> None:
        """Set the bankroll amount directly in the stats dictionary."""
        if new_amount < 0:
            raise OutOfMoneyException(f"Bankroll cannot be negative. Attempted to set: {new_amount}")

        self.stats["bankroll"] = new_amount

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
        if result_tuple[0] == Result.VICTORY:
            if result_tuple[1] > 0:
                self.stats.update({"wins": self.stats.get("wins") + 1})
                self.bankroll += result_tuple[1]
                return True
            else:
                return False
        elif result_tuple[0] == Result.PUSH:
            self.stats.update({"pushes": self.stats.get("pushes") + 1})
            return True
        else:
            if 0 > result_tuple[1] >= -self.bankroll:
                self.stats.update({"losses": self.stats.get("losses") + 1})
                self.bankroll += result_tuple[1]
                return True
            else:
                return False

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
        if self.bankroll == 0:

            raise OutOfMoneyException("You're broke! Please add more money to your bankroll!")
        bet = None
        while not bet:
            try:
                print(f"Ante up! Your current bankroll is {self.bankroll}.")
                bet = int(input(f"Please enter a number between 1 and {self.bankroll}:\t"))
                if bet > self.bankroll:
                    bet = None
            except Exception:
                print("Please enter an integer!")
        self.bet = bet

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
        if self.bet <= self.bankroll / 2:
            self.bet *= 2
            return True
        else:
            return False

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
        print("Please take your turn")
        result = None
        while not result:
            move = input("Enter 'Hit', 'Stand' or 'Double Down': ")
            move = move.strip()
            move = move.lower()
            if move == "hit":
                self.hand.add_card(deck.pop())
                result = Move.HIT
            elif move == "stand":
                result = Move.STAND
            elif move == "double down":
                if self.double_down():
                    self.hand.add_card(deck.pop())
                    result = Move.DOUBLE_DOWN
                else:
                    print("You don't have enough money to double down.")
        return result

    def __eq__(self, other):
        return self.stats == other.stats


def load_player(path: Path) -> Player:
    with open(path, "r") as file:
        stats = json.load(file)
    return Player(stats)


def save_player(player: Player, path: Path, ) -> None:
    with open(path, "w") as file:
        json.dump(player.stats, file)
