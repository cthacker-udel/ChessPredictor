from secrets import randbelow
from enum import Enum


class CoinFace(Enum):
    """
    Represents the face of a coin, can either be heads or tails
    """
    HEADS = 0
    TAILS = 1


def flip_coin() -> CoinFace:
    """
    Flips a coin, either returning Heads or Tails
    :return: The CoinFace enum equivalent of the coin flip
    """
    return CoinFace(randbelow(2))
