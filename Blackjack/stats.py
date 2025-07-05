"""
Stats handles the fileIO of tracking a player

Stats should include: Wins, Losses, Bankroll

"""


class Stats:
    def __init__(self, starting_bankroll):
        self.stats = {
            "bankroll": starting_bankroll,
            "wins": 0,
            "losses": 0,
        }

    def get_wins(self):
        pass

    def get_losses(self):
        pass

    def get_bankroll(self):
        pass

    def save(self, name):
        pass

    def load(self, name):
        pass

    def add_win(self):
        pass

    def add_loss(self):
        pass

    def adjust_bankroll(self, change):
        pass
