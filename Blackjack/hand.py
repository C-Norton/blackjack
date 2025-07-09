import collections

from .card import Card
from .value import Value


class Hand:
    def __init__(self):
        self.cards = collections.deque()

    def add_card(self, my_card: Card):
        self.cards.appendleft(my_card)

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
