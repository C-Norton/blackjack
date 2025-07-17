import collections

from .card import Card
from .value import Value


def _handle_aces(subtotal: int, aces: int) -> int:
    """
    Handles the point value of aces, which are counted as 11, unless it would cause the player to bust, in which case
    they are, one by one, converted to ones.
    Being a private method, this does not have to be implemented by the student, though it's implementation is suggested
    :param subtotal: the total value excluding aces
    :param aces: The number of aces in the hand
    :return: the final total of the hand
    """
    if aces + subtotal <= 11 and aces > 0:
        return subtotal + 10 + aces
    else:
        return subtotal + aces


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
        :return:returns the number of cards in the cards collection
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
        total: int = 0
        aces: int = 0

        for card in self.cards:
            card_value = card.value
            if not card_value == Value.ACE:
                total += card_value.score
            else:
                aces += 1

        total = _handle_aces(total, aces)

        return total

    def __str__(self):
        return "\n".join(str(card) for card in self.cards)

    def __getitem__(self, index):
        return self.cards[index]
