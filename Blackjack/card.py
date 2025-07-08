from .suit import Suit
from .value import Value


class Card:
    """
    __init__ is a method that creates an instance of a class; in this case a card. It's double underscord (dunder) name
    It takes in two external parameters, suit and value is reserved, no other method may use this name, it always
    creates and returns a fresh instance

    Suit and Value are both enum parameters that confer the card's identity, such as the ace of spades.
    """
    def __init__(self, suit: Suit, value: Value):
        self.Suit = suit
        self.Value = value
        self.FaceDown = False
    """
    is_facedown determines if the card is face-down on the table, which changes it's __str__ method. this should only
    ever be the first card dealt to the dealer's hand.
    """
    def is_facedown(self):
        return self.FaceDown
    """
    Flip simply inverts the card facedown value. It's a setter method
    """
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
