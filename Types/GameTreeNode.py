from __future__ import annotations
from typing import List

from Game import Game


class GameTreeNode:
    """
    Represents a node in the tree, only contains a value.
    """

    def __init__(self: GameTreeNode, value: Game) -> None:
        """
        Initializes a new GameTreeNode instance with the Game snapshot supplied

        :param value: A snapshot of the current game instance
        """
        self.numerator = 0
        self.denominator = 1
        self.value = value
        self.children: List[GameTreeNode] = []
        self.parent: GameTreeNode | None = None

    def add_child(self: GameTreeNode, child: GameTreeNode) -> GameTreeNode:
        """
        Adds a child to this GameTreeNode instance

        :param child: The child to be added
        :return: The GameTreeNode instance with the modified children
        """
        child.parent = self
        self.children.append(child)
        return self
