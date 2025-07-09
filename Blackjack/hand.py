import collections

from .card import Card
from .value import Value


class Hand:
    def __init__(self):
        """
        __init__ creates a new hand
        """
        self.cards = collections.deque()

    def add_card(self, card: Card)->None:
        """
        :param card: the card to add to the collection
        :return:
        """
        self.cards.appendleft(card)

    def get_size(self):
        return len(self.cards)

    def get_total(self):
        total = 0
        aces = 0

        for card in self.cards:
            card_value = card.get_value()
            if not card_value == Value.ACE:
                total += card_value.score
            else:
                aces += 1

        total = self.handle_aces(total, aces)

        return total

    def handle_aces(self, subtotal: int, aces: int) -> int:
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