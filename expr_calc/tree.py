from typing import List

from expr_calc.operators import op_map
from expr_calc.token import Token, TokenType


class Tree:

    def __init__(self, node: Token, children: List["Tree"] = None) -> None:
        self.node: Token = node
        self.children: List[Tree] = children if children else []
        self.queue = []

    def set_node(self, val: Token) -> None:
        self.node = val

    def append_child(self, child: "Tree") -> None:
        self.children.append(child)

    def traverse(self, queue=None):
        if queue is None:
            queue = []

        for sub in self.children:
            if not sub:
                break
            sub.traverse(queue=queue)
        print(self.node)
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

    def __repr__(self) -> str:
        return f"{self.node} -> {self.children} "