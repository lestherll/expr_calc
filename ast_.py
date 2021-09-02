from expr_calc.calc import Token, TokenType, Calc

from itertools import chain
from collections import deque

from typing import List, Optional, Union


class Tree:

    def __init__(self, node: Token, children: List["Tree"]) -> None:
        self.node: Optional[Token] = node
        self.children: List[Tree] = children
        self.queue = deque()

    def traverse(self, queue=deque()):
        queue = queue
        for sub in self.children:
            if not sub:
                break
            sub.traverse(queue=queue)
        print(self.node)
        queue.append(self.node)
        return queue
        # self.queue.append(self.val)

    def eval(self):
        self.queue = self.traverse()
        stack = []
        for type_, val in self.queue:
            if type_ is TokenType.NUMBER:
                stack.append(val)
            elif type_ is TokenType.BINARY_OP:
                # res = reduce(Calc.op_map[val], stack)
                # stack.clear()
                # stack.append(res)
                op = Calc.op_map[val]
                while len(stack) > 1:
                    stack.append(op(stack.pop(), stack.pop()))
            elif type_ is TokenType.UNARY_OP:
                stack.append(Calc.unary_op_map[val](stack.pop()))
        return stack[0]

    def __iter__(self):
        return iter(chain((self.node, ), self.children))

    def __repr__(self):
        return f"{self.node} [\n\t{self.children if self.children else ''}]"

root = Tree(Token(TokenType.BINARY_OP, "-"), [
    Tree(Token(TokenType.NUMBER, 12), []),
    Tree(Token(TokenType.NUMBER, 12), []),
    Tree(Token(TokenType.UNARY_OP, "-"), [
        Tree(Token(TokenType.NUMBER, 23), [])
    ])
])

# root.traverse()
print(root)
print(root.eval())
