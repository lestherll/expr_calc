from typing import List, Iterable
from collections import deque

from expr_calc.operators import op_map
from expr_calc.token import Token, TokenType


class Tree:

    def __init__(self, node: Token, children: Iterable["Tree"] = None) -> None:
        self.node: Token = node
        self.children: deque[Tree] = deque(children) if children else deque()
        self.queue = deque()

    def set_node(self, val: Token) -> None:
        self.node = val

    def append_child(self, child: "Tree") -> None:
        self.children.append(child)

    def appendleft_child(self, child: "Tree") -> None:
        self.children.appendleft(child)

    def traverse(self, queue=None):
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

        # a leaf must always be a number
        if self.node.type_ is TokenType.NUMBER:
            return self.node.val

        elif self.node.type_ is TokenType.BINARY_OP:
            operand_a, operand_b = self.children
            return op_map[self.node.val](operand_a.eval(), operand_b.eval())

        elif self.node.type_ is TokenType.UNARY_OP and self.node.val == "-":
            return self.children[0].eval() * -1

    def __eq__(self, other: "Tree"):
        if not isinstance(other, Tree):
            return False
        else:
            return all([i == j for i, j in zip(self.traverse(), other.traverse())])

    def __repr__(self) -> str:
        if self.children:
            return f"{self.node} -> {[child for child in self.children]} "
        else:
            return f"{self.node}"
