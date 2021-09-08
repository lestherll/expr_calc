from decimal import Decimal, getcontext

from expr_calc.errors import NoProgramLoaded, ExcessiveDotError, TokenError
from expr_calc.token import Token, TokenType
from expr_calc.operators import OP_LIST, unary_op_map
from expr_calc.tree import Tree
from expr_calc.lexer import Lexer

from typing import List, Optional


class Calc:

    def __init__(self, program: str = "") -> None:
        """
        Calculator Object for interpreting expressions

        :param program: expression, also called program,
         to be interpreted
        """
        self.program = program
        self.stack = []

        self.lexed = []
        self.shunted = []
        self.tree: Optional[Tree] = None

        self.lexer: Lexer = Lexer(self.program)

    def lex(self, program: str = "") -> List[Token]:
        if program and not program.isspace():
            self.program = program

        if self.program.isspace() or not self.program:
            raise NoProgramLoaded("No expression loaded\n")

        self.lexed = self.lexer.lex(self.program)  # update self.lexed
        return self.lexed

    def parse(self, program: str = "") -> Tree:
        """
        Parses the program given in order to create an abstract
        syntax tree that can be evaluated into a value

        :param program: optional program to be parsed
        :return: abstract syntax tree for the expression passed
        """

        if program and not program.isspace():
            lexed = self.lex(program=program)
        else:
            lexed = self.lex()

        tree_stack: List[Tree] = []     # used to build ast
        op_tree_stack: List[Tree] = []   # temporary op tree

        for token in lexed:

            if token.type_ is TokenType.NUMBER:
                tree_stack.append(Tree(token))

            elif token.type_ is TokenType.BINARY_OP:
                # make operands child node of the bin op
                # if bin op is the same as prev, make the
                # prev's operands a child node of the current bin op

                # check if curr bin op has less or equal
                # precedence than ones in the operator stack
                # if the operator stack is not empty
                while op_tree_stack and op_tree_stack[-1].node.val in OP_LIST and\
                        OP_LIST[op_tree_stack[-1].node.val] >= OP_LIST[token.val]:

                    curr_node = op_tree_stack.pop()
                    while tree_stack:
                        curr_node.append_child(tree_stack.pop())
                    tree_stack.append(curr_node)
                op_tree_stack.append(Tree(token))

            elif token.type_ is TokenType.UNARY_OP:
                op_tree_stack.append(Tree(token))

            elif token.type_ is TokenType.L_PAREN:
                op_tree_stack.append(Tree(token))

            elif token.type_ is TokenType.R_PAREN:
                while op_tree_stack and op_tree_stack[-1].node.val != "(":

                    curr_node = op_tree_stack.pop()
                    if curr_node.node.type_ is TokenType.BINARY_OP:
                        curr_node.appendleft_child(tree_stack.pop())
                        curr_node.appendleft_child(tree_stack.pop())
                    else:
                        curr_node.appendleft_child(tree_stack.pop())

                    tree_stack.append(curr_node)
                op_tree_stack.pop()

        while op_tree_stack:

            curr_node = op_tree_stack.pop()
            if curr_node.node.type_ is TokenType.BINARY_OP:
                curr_node.appendleft_child(tree_stack.pop())
                curr_node.appendleft_child(tree_stack.pop())
            else:
                curr_node.appendleft_child(tree_stack.pop())
            tree_stack.append(curr_node)

        self.tree = tree_stack[0] if tree_stack else None
        return self.tree

    def eval(self) -> float:
        """
        Lexes the program, parses it, and the evaluates it
        to a single value

        :return: final value
        """
        self.lex()
        self.parse()
        return self.tree.eval()

    def repl(self) -> None:
        """
        Run a REPL to evaluate expressions on the fly
        :return: None
        """
        print("WELCOME TO EXPRESSION INTERPRETER!")
        # self.program = 1
        while True:
            try:
                self.program = input("calc> ")

                if self.program == "q":
                    print("goodbye")
                    break

                print(self.eval(), end="\n\n")
            except NoProgramLoaded as npl:
                print(npl)
            except TokenError as te:
                print(te)
            except ExcessiveDotError as ede:
                print(ede)
