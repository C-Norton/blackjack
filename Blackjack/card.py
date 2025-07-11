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
        __str__ is a method that returns a string representation of the card
        :return:
        """
        if not self.face_down:
            return self.value.display + str(self.suit)
        else:
            return "##"
