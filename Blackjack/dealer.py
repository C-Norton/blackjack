"""
The dealer is responsible for his own moves, and the game is responsible for
giving the dealer cards, and requesting a move from the dealer

The dealer should have a hand, which should have the first card face down.
The dealer knows the value of the card

The dealer hits on anything below 17.

The dealer's external interface should consist of

take_turn(Deck)
reveal_hand() (flips all cards and prints)
print_hand()  (prints including face down
"""

from .hand import Hand
from .move import Move


class Dealer:
    def __init__(self, dealer_hand=Hand()):
        self.hand = dealer_hand

    def reveal_hand(self):
        pass

    def print_hand(self):
        pass

    def take_turn(self, deck):
        if self.hand.get_size() < 2:
            card = deck.popleft()
            if self.hand.get_size() == 1:
                card.flip()
            self.hand.add_card(card)
            return Move.HIT
        elif self.hand.get_total() < 17:
            self.hand.add_card(deck.popleft())
            return Move.HIT
        else:
            return Move.STAND
