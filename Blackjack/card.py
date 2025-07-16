"""
Card represents a card in a game of blackjack. It has a suit, and a value. It may be placed face up or face down on the
table, and may be flipped during play.
"""
from .suit import Suit
from .value import Value

class Card:
    def __init__(self, suit: Suit, value: Value):
        """
        __init__ is a method that creates an instance of a class; in this case a card. It's double underscord (dunder) name
        It takes in two external parameters, suit and value is reserved, no other method may use this name, it always
        creates and returns a fresh instance

        :param suit: An enum parameter representing the suit of the card
        :param value: An enum parameter representing the value of the card
        """
        self.suit: Suit = suit
        self.value: Value = value
        self.face_down: bool = False

    def __str__(self):
        """
        __str__ is a method that returns a string representation of the card. This should take the format value suitIcon
        or ## if the card is facedown. For instance J♥ for the jack of hearts
        :return: String
        """
        if not self.face_down:
            return str(self.value) + str(self.suit)
        else:
            return "##"
