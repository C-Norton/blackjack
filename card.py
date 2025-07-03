from suit import Suit
from value import Value


class Card:
    def __init__(self, suit: Suit, value: Value):
        self.Suit = suit
        self.Value = value
        self.FaceDown = False

    def is_facedown(self):
        return self.FaceDown

    def flip(self):
        self.FaceDown = not self.FaceDown

    def get_value(self):
        return self.Value

    def get_suit(self):
        return self.Suit

    def __str__(self):
        if not self.FaceDown:
            return self.Value.display + str(self.Suit)
        else:
            return "##"