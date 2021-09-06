from typing import Iterable
from collections import deque

from expr_calc.operators import op_map
from expr_calc.token import Token, TokenType


class Tree:

    def __init__(self, node: Token, children: Iterable["Tree"] = None) -> None:
        """
        Initialise a Tree object with its value and optional children
        :param node: value of the node itself
        :param children: children of the node if any, children must be Tree objects.
        """
        self.node: Token = node
        self.children: deque[Tree] = deque(children) if children else deque()
        self.queue = deque()

    def set_node(self, val: Token) -> None:
        """
        Set a node to a token val
        :param val:
        :return:
        """
        self.node = val

    def append_child(self, child: "Tree") -> None:
        """
        Append a child to right of a Tree object
        :param child: child to be appended
        :return:
        """
        self.children.append(child)

    def appendleft_child(self, child: "Tree") -> None:
        """
        Append a child to the left of a Tree object
        :param child: child to be appended
        :return:
        """
        self.children.appendleft(child)

    def traverse(self, queue=None):
        """
        Traverse the tree(postorder), its children, and their children, recursively
        and set them to self.queue

        :param queue:
        :return:
        """
        if queue is None:
            queue = deque()

        for sub in self.children:
            if not sub:
                break
            sub.traverse(queue=queue)
        # print(self.node)
        queue.append(self.node)
        return queue

    def eval(self) -> float:
        """
        Recursively evaluate the tree to its final value
        :return: final value
        """

        # a leaf must always be a number
        if self.node.type_ is TokenType.NUMBER:
            return self.node.val

        elif self.node.type_ is TokenType.BINARY_OP:
            operand_a, operand_b = self.children
            return op_map[self.node.val](operand_a.eval(), operand_b.eval())

        elif self.node.type_ is TokenType.UNARY_OP and self.node.val == "-":
            return self.children[0].eval() * -1

    def __eq__(self, other: "Tree") -> bool:
        """
        A tree is equal to another tree if the nodes are the same
        :param other: other tree to be compared
        :return: if self is equal to other
        """
        if not isinstance(other, Tree):
            return False
        else:
            return all([i == j for i, j in zip(self.traverse(), other.traverse())])

    def __repr__(self) -> str:
        if self.children:
            return f"{self.node} -> {[child for child in self.children]} "
        else:
            return f"{self.node}"
