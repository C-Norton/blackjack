"""
Player represents the IO necessary to collect move information from the player,
as well as the hand management of the player.

player has 2 fields initialized by the constructor,
bankroll, which represents the amount of money the player has
and name, which reflects the player's name.
"""

from pathlib import Path

from .move import Move
from .result import Result
import json


class OutOfMoneyException:
    pass


# todo: properties for stats
class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.stats = dict(
            {
                "name": name,
                "bankroll": bankroll,
                "wins": 0,
                "losses": 0,
                "pushes": 0,
            }
        )
        self.bet = 0
        self.hand = None

    def get_name(self):
        return self.name

    def deal_card(self, card):
        pass

    def get_stats(self):
        return self.stats

    def get_bankroll(self):
        return self.bankroll

    def update_bankroll(self, net_change):
        if net_change >= 0:
            self.bankroll += net_change
            self.stats.adjust_bankroll(net_change)
            return True
        elif net_change < 0 and -1 * net_change <= self.bankroll:
            self.bankroll += net_change
            self.stats.adjust_bankroll(net_change)
            return True
        else:
            print(
                f"Error, cannot adjust bankroll by{net_change} as bankroll is equal to {self.bankroll}"
            )
            return False

    def update_stats(self, result_tuple):
        if result_tuple[0] == Result.VICTORY:
            if result_tuple[1] > 0:
                self.stats.add_win()
                self.stats.adjust_bankroll(result_tuple[1])
                return True
            else:
                return False
        elif result_tuple[0] == Result.PUSH:
            self.stats.add_push()
            return True
        else:
            if 0 > result_tuple[1] >= -self.bankroll:
                self.stats.add_loss()
                self.stats.adjust_bankroll(result_tuple[1])
                return True
            else:
                return False

    def ante(self):
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
            except:
                print("Please enter an integer!")
        self.bet = bet

    def get_bet(self):
        return self.bet

    def double_down(self):
        if self.bet <= self.bankroll / 2:
            self.bet *= 2
            return True
        else:
            return False

    def take_turn(self, deck):
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
                    self.hand.add_card(deck.pop)
                    result = Move.DOUBLE_DOWN
                else:
                    print("You don't have enough money to double down.")
        return result

    def has_busted(self):
        return self.hand.get_total() > 21

    def get_hand(self):
        return self.hand


def load_player(path):

    with open(path, "r") as file:
        return json.load(file)


def save_player(
    player: Player,
    path,
):
    with open(path, "w") as file:
        json.dump(player.stats, file)
