# from expr_calc.tree import Tree
from collections import deque

from expr_calc.errors import NoProgramLoaded
from expr_calc.token import Token, TokenType
from expr_calc.operators import OP_LIST, unary_op_map

from typing import List, Optional

from expr_calc.tree import Tree


class Calc:

    def __init__(self, program: str = "") -> None:
        """
        Initialise a Calc instance/object

        Args:
            program (str, optional): Program to be interpreted. Defaults to None.
        """
        self.program = program
        self.stack = []

        self.lexed = []
        self.shunted = []
        self.tree: Optional[Tree] = None

    def tokenise(self, lexeme: str) -> Optional[TokenType]:
        """
        Helper function for mapping lexeme or characters or
        strings into their respective token equivalent

        Args:
            lexeme (str): string to be mapped to token

        Returns:
            TokenType: resulting token of the lexeme
        """
        if lexeme.isdigit():
            return TokenType.NUMBER
        elif lexeme in OP_LIST:
            return TokenType.BINARY_OP
        elif lexeme == "(":
            return TokenType.L_PAREN
        elif lexeme == ")":
            return TokenType.R_PAREN

    def lex(self, program: str = "") -> List[Token]:
        """Lexes the program given or at self.program

        Args:
            program (str, optional): Optional program. Defaults to None.

        Returns:
            List[Token]: [description]
        """

        if program and not program.isspace():
            self.program = program

        tokens: List[Token] = []
        program_length = len(self.program)  # will fail if self.program is None as well
        temp_digit = []  # stack for digit chars and decimal sign
        digit_flag = False  # flag when digit is encountered

        for i, char in enumerate(self.program):
            token = self.tokenise(char)
            if token is TokenType.NUMBER:
                temp_digit.append(char)

                # checks if current char which is a number is the last char
                if i + 1 == program_length:
                    tokens.append(Token(TokenType.NUMBER, float("".join(temp_digit))))
                digit_flag = True

            else:
                if digit_flag:
                    if char == ".":
                        temp_digit.append(char)
                    else:
                        tokens.append(Token(TokenType.NUMBER, float("".join(temp_digit))))
                        temp_digit.clear()
                        digit_flag = False

                if token is TokenType.BINARY_OP:
                    if char in unary_op_map and (not tokens or tokens[-1].type_ is not TokenType.NUMBER):
                        temp_index = i
                        while temp_index+1 < program_length:
                            if self.tokenise(self.program[temp_index+1]) in\
                                    (TokenType.L_PAREN, TokenType.NUMBER, TokenType.BINARY_OP):
                                tokens.append(Token(TokenType.UNARY_OP, char))
                                break
                            temp_index += 1
                        # temp_digit.append(char)
                    else:
                        tokens.append(Token(TokenType.BINARY_OP, char))

                if token in (TokenType.L_PAREN, TokenType.R_PAREN):
                    tokens.append(Token(token, char))

        self.lexed = tokens  # update self.lexed

        return tokens

    def parse(self, program: str = "") -> Tree:
        """Uses the result of the lexer to generate
        expressions from infix to postfix

        Args:
            program (str, optional): program to be evaluated. Defaults to None.

        Returns:
            List: [description]
        """

        if program and not program.isspace():
            lexed = self.lex(program=program)
        else:
            lexed = self.lex()

        tree_stack: List[Tree] = []     # used to build ast
        op_tree_stack: List[Tree] = []   # temporary op tree

        prev_bin_op = None
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

                prev_bin_op = token.val

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

        self.tree = tree_stack[0]
        return tree_stack[0]

    def eval(self) -> float:
        self.lex()
        self.parse()
        return self.tree.eval()

    def repl(self) -> None:
        """
        Runs a REPL which evaluates programs and expressions
        """
        print("WELCOME TO CALCULATOR LANGUAGE!")
        # self.program = 1
        while True:
            try:
                self.program = input("> ")

                if self.program == "q":
                    print("goodbye")
                    break

                print(self.eval(), end="\n\n")
            except NoProgramLoaded as npl:
                print(npl)
