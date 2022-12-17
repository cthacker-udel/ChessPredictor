from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Types.GameTreeNode import GameTreeNode


class GameTree:
    """
    Represents a game tree, https://en.wikipedia.org/wiki/Game_tree, the one being used for chess in this instance will
    be utilizing the minmax algorithm, set to 10 plies ahead, and utilizing as well the alpha-beta pruning to maximize
    the efficiency of analyzing the tree.
    """

    def __init__(self: GameTree) -> None:
        """
        Initializes a GameTree instance with a root equal to None
        """
        self.root: GameTreeNode | None = None

    def set_root(self, node: GameTreeNode):
        """
        Sets the root of the tree

        :param node: The node to instantiate the tree with
        :return: The tree instance
        """
        self.root = node
        return self

