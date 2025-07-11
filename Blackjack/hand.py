import collections

from .card import Card
from .value import Value


class Hand:
    def __init__(self):
        """
        __init__ creates a new hand
        """
        self.cards = collections.deque()

    def add_card(self, card: Card) -> None:
        """
        :param card: the card to add to the collection
        :return:
        """
        self.cards.appendleft(card)

    def get_size(self) -> int:
        """
        :return:returns the size of the cards collection
        """
        return len(self.cards)

    def get_total(self) -> int:
        """
        Get total calculates the point value of the hand as follows
        Numbered cards: The value of their number
        Face cards (jack king queen): Ten
        Aces: 11, unless 11 would cause you to bust, in which case 1.
        :return: the point value of the hand
        """
        total = 0
        aces = 0

        for card in self.cards:
            card_value = card.value
            if not card_value == Value.ACE:
                total += card_value.score
            else:
                aces += 1

        total = self._handle_aces(total, aces)

        return total

    def _handle_aces(self, subtotal: int, aces: int) -> int:
        """
        Handles the point value of
        :param subtotal:
        :param aces:
        :return:
        """
        if aces + subtotal <= 11 and aces > 0:
            return subtotal + 10 + aces
        else:
            return subtotal + aces

    def __str__(self):
        output = ""
        for card in self.cards:
            output += str(card) + "\n"
        return output.strip("\n")

    def __getitem__(self, index):
        return self.cards[index]
