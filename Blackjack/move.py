"""
A move is an enum that gives a move result, Hit, Stand, Double down, split if implemented
"""

from enum import Enum


class Move(Enum):
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
