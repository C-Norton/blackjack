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
        self.stats = Stats()
        self.hand = None

    def get_name(self):
        return self.name

    def get_stats(self):
        return self.stats.get_statistics()

    def get_bankroll(self):
        return self.bankroll
