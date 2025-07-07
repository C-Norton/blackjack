"""
Player represents the IO necessary to collect move information from the player,
as well as the hand management of the player.

player has 2 fields initialized by the constructor,
bankroll, which represents the amount of money the player has
and name, which reflects the player's name.
"""

from .result import Result
from .stats import Stats


class Player:
    def __init__(self, name, bankroll, stats=None):
        self.name = name
        self.bankroll = bankroll
        self.stats = stats if stats is not None else Stats(bankroll)
        self.bet = 0
        self.hand = None

    def get_name(self):
        return self.name

    def deal_card(self, card):
        pass

    def get_stats(self):
        print(f"============== Stats for {self.name} ==============")
        print("Total Money: " + self.stats.get_bankroll())
        print("Total Wins: " + self.stats.get_wins())
        print("Total Losses: " + self.stats.get_losses())

    def get_bankroll(self):
        return self.bankroll

    def update_bankroll(self, net_change):
        self.bankroll += net_change

    def update_stats(self, result_tuple):
        if result_tuple(0) == Result.VICTORY:
            self.stats.add_win()
            self.stats.adjust_bankroll(result_tuple(1))
        elif result_tuple(0) == Result.PUSH:
            self.stats.add_push()
        else:
            self.stats.add_loss()
            self.stats.adjust_bankroll(-result_tuple(1))

    def ante(self):
        pass

    def get_bet(self):
        return self.bet

    def double_down(self):
        pass

    def can_double_down(self):
        pass

    def take_turn(self, deck):
        pass

    def has_busted(self):
        pass

    def get_hand(self):
        return None
