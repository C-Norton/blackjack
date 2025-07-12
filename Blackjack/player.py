"""
Player represents the IO necessary to collect move information from the player,
as well as the hand management of the player.

player has 2 fields initialized by the constructor,
bankroll, which represents the amount of money the player has
and name, which reflects the player's name.
"""

import collections
import json
from pathlib import Path
from typing import Optional

from .hand import Hand
from .move import Move
from .result import Result


class OutOfMoneyException:
    print("The house always wins!")


class Player(game_participant):
    def __init__(self, stats: dict):
        self.name: str = stats["name"]
        self.bankroll: int = stats["bankroll"]
        self.stats: dict = stats
        self.bet: int = 0
        self.hand: Optional[Hand] = None

    @classmethod
    def from_name_bankroll(cls, name: str, bankroll: int):
        return Player(
            {
                "name": name,
                "bankroll": bankroll,
                "wins": 0,
                "losses": 0,
                "pushes": 0,
            }
        )

    def deal_card(self, card):
        self.hand.add_card(card)

    def update_bankroll(self, net_change) -> bool:
        if net_change >= 0:
            self.bankroll += net_change
            self.stats.update({"bankroll": self.bankroll})
            return True
        elif net_change < 0 and -1 * net_change <= self.bankroll:
            self.bankroll += net_change
            self.stats.update({"bankroll": self.bankroll})
            return True
        else:
            print(
                f"Error, cannot adjust bankroll by{net_change} as bankroll is equal to {self.bankroll}"
            )
            return False

    def update_stats(self, result_tuple) -> bool:
        if result_tuple[0] == Result.VICTORY:
            if result_tuple[1] > 0:
                self.stats.update({"wins": self.stats.get("wins") + 1})
                self.stats.update(
                    {"bankroll": self.stats.get("bankroll") + result_tuple[1]}
                )
                return True
            else:
                return False
        elif result_tuple[0] == Result.PUSH:
            self.stats.update({"pushes": self.stats.get("pushes") + 1})
            return True
        else:
            if 0 > result_tuple[1] >= -self.bankroll:
                self.stats.update({"losses": self.stats.get("losses") + 1})
                self.stats.update(
                    {"bankroll": self.stats.get("bankroll") + result_tuple[1]}
                )
                return True
            else:
                return False

    def ante(self) -> int:
        if self.bankroll == 0:
            # This behavior is not defined by tests. We will leave this edge case alone, as we don't want to be too
            # picky for the students
            print("You're broke! Please add more money to your bankroll!")
            raise OutOfMoneyException
        bet = None
        while not bet:
            try:
                print(f"Ante up! Your current bankroll is {self.bankroll}.")
                bet = int(
                    input(f"Please enter a number between 1 and {self.bankroll}:\t")
                )
                if bet > self.bankroll:
                    bet = None
            except Exception:
                print("Please enter an integer!")
        self.bet = bet

    def double_down(self) -> bool:
        if self.bet <= self.bankroll / 2:
            self.bet *= 2
            return True
        else:
            return False

    def take_turn(self, deck: collections.deque) -> Move:
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


def save_player(
    player: Player,
    path: Path,
):
    with open(path, "w") as file:
        json.dump(player.stats, file)
