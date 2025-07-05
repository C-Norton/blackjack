"""
Player represents the IO necessary to collect move information from the player,
as well as the hand management of the player.

player has 2 fields initialized by the constructor,
bankroll, which represents the amount of money the player has
and name, which reflects the player's name.
"""

from .stats import Stats


class Player:
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.stats = Stats(bankroll)
        self.hand = None

    def get_name(self):
        return self.name

    def get_stats(self):
        return self.stats.get_statistics()

    def get_bankroll(self):
        return self.bankroll

    def update_bankroll(self, net_change):
        self.bankroll += net_change

    def update_stats(self, result_tuple):
        pass

    def ante(self):
        pass

    def take_turn(self, deck):
        pass

    def has_busted(self):
        pass

    def get_hand(self):
        return None
