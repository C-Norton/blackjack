import collections
from abc import abstractmethod, ABC

from .card import Card
from .result import Result


class GameParticipant(ABC):

    def __init__(self):
        self.hand = None

    @abstractmethod
    def take_turn(self, deck: collections.deque) -> Result:
        """
        An abstract method to be implemented by subclasses that defines how a turn
        is taken within the game. It processes the given deck and produces a result
        representing the outcome of the turn.

        Args:
            deck (collections.deque): A deck of cards which is manipulated during
            the turn. The specific operations or modifications depend on the
            implementation in the subclass.

        Returns:
            Result: The outcome of processing the turn, determined by the subclass's
            implementation.
        """
        pass
    def has_busted(self) -> bool:
        """
        Determine if the hand's total exceeds the allowed limit (busted).

        Checks the total value of the hand to determine if it has gone
        over the predefined limit, indicating that the hand is busted.

        Returns:
            bool: True if the hand's value exceeds the allowable limit,
            False otherwise.
        """
        return self.hand.get_total() > 21
    @abstractmethod
    def deal_card(self, card:Card) -> None:
        """
        Provide an interface for dealing cards in blackjack.

        This method is intended to be an abstract method that must be implemented in
        subclasses. It represents the functionality to handle dealing a card within
        the game logic.

        Args:
            card: The card object to be dealt. It should contain all necessary
                properties and methods to represent a card.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass