from enum import Enum


class Suit(Enum):
    SPADES = (0, "♠")
    DIAMONDS = (1, "♦")
    CLUBS = (2, "♣")
    HEARTS = (3, "♥")

    def __init__(self, index, display):
        self.display = display
        self.index = index

    def __str__(self):
        return self.display
