import collections
from abc import abstractmethod, ABC

from .result import Result


class GameParticipant(ABC):

    def __init__(self):
        self.hand = None

    @abstractmethod
    def take_turn(self, deck: collections.deque) -> Result:
        pass
    def has_busted(self) -> bool:
        return self.hand.get_total()>21