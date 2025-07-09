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
        self._face_down: bool = False

    @property
    def face_down(self):
        """
        this is a property method that returns True if the card face down
        :return:
        """
        return self._face_down

    @face_down.setter
    def face_down(self, value):
        """
        this is a property method that sets the value of the face down variable
        :param value:
        :return:
        """
        self._face_down = value

    def __str__(self):
        """
        __str__ is a method that returns a string representation of the card
        :return:
        """
        if not self._face_down:
            return self.value.display + str(self.suit)
        else:
            return "##"
