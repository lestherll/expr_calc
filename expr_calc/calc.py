# from expr_calc.tree import Tree
from expr_calc.errors import NoProgramLoaded
from expr_calc.token import Token, TokenType
from expr_calc.operators import OP_LIST, op_map, unary_op_map

from typing import List, Optional


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

    def shunt(self, program: str = "") -> List[Token]:
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

        operators = []
        output = []

        tree_stack = []     # used to build ast
        temp_op_tree = []   # temporary op tree

        prev_bin_op = None
        for token in lexed:

            if token.type_ is TokenType.NUMBER:
                output.append(token)
                tree_stack.append(Tree(token))

            elif token.type_ is TokenType.BINARY_OP:
                # make operands child node of the bin op
                # if bin op is the same as prev, make the
                # prev's operands a child node of the current bin op

                # check if curr bin op has less or equal
                # precedence than ones in the operator stack
                # if the operator stack is not empty
                while operators and operators[-1].val in OP_LIST and OP_LIST[operators[-1].val] >= OP_LIST[token.val]:
                    curr_op = operators.pop()
                    output.append(curr_op)  # pop operators from operator stack to output

                    curr_node = temp_op_tree.pop()
                    while tree_stack:
                        curr_node.append_child(tree_stack.pop())
                    # curr_node.append_child(tree_stack.pop())
                    # curr_node.append_child(tree_stack.pop())
                    tree_stack.append(curr_node)
                operators.append(token)

                temp_op_tree.append(Tree(token))

                prev_bin_op = token.val

            elif token.type_ is TokenType.UNARY_OP:
                operators.append(token)
                temp_op_tree.append(Tree(token))

            elif token.type_ is TokenType.L_PAREN:
                operators.append(token)
                temp_op_tree.append(Tree(token))

            elif token.type_ is TokenType.R_PAREN:
                while operators and operators[-1].val != "(":
                    output.append(operators.pop())

                    curr_node = temp_op_tree.pop()
                    if curr_node.node.type_ is TokenType.BINARY_OP:
                        curr_node.append_child(tree_stack.pop())
                        curr_node.append_child(tree_stack.pop())
                    else:
                        curr_node.append_child(tree_stack.pop())

                    tree_stack.append(curr_node)
                operators.pop()
                temp_op_tree.pop()

        while operators:
            output.append(operators.pop())

            curr_node = temp_op_tree.pop()
            if curr_node.node.type_ is TokenType.BINARY_OP:
                curr_node.append_child(tree_stack.pop())
                curr_node.append_child(tree_stack.pop())
            else:
                curr_node.append_child(tree_stack.pop())
            tree_stack.append(curr_node)

        self.tree = tree_stack[0]
        self.shunted = output

        # self.tree.traverse()
        x = self.tree.eval()

        return output

    # def eval(self, program: str = "", infix: bool = True) -> float:
    #     """
    #     Iterate through the lexed program and evaluates it
    #
    #     Returns:
    #         float: Result of the program
    #     """
    #     if program and not program.isspace():
    #         self.program = program
    #
    #     if not self.program or self.program.isspace():
    #         raise NoProgramLoaded("No program loaded\n")
    #
    #     self.lex()
    #     if infix is True:
    #         self.shunt()
    #         processed = self.shunted
    #     else:
    #         processed = self.lexed
    #
    #     self.stack.clear()
    #     unary_minus_flag: bool = False
    #     for type_, val in processed:
    #         if type_ is TokenType.NUMBER:
    #             if unary_minus_flag:
    #                 self.stack.append(-val)
    #             else:
    #                 self.stack.append(val)
    #         else:
    #             if type_ is TokenType.BINARY_OP:
    #                 if len(self.stack) >= 2:
    #                     a = self.stack.pop()
    #                     b = self.stack.pop()
    #                     res = op_map[val](a, b)
    #                     self.stack.append(res)
    #             elif self.stack and type_ is TokenType.UNARY_OP and val == "-":
    #                 self.stack.append(self.stack.pop() * -1)
    #
    #     return self.stack[0]

    def eval(self) -> float:
        self.lex()
        self.shunt()
        return self.tree.eval()

    def repl(self, infix=True) -> None:
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

                print(self.eval(infix=infix), end="\n\n")
            except NoProgramLoaded as npl:
                print(npl)


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

        # the leaf must always be a number
        if self.node.type_ is TokenType.NUMBER:
            return self.node.val

        elif self.node.type_ is TokenType.BINARY_OP:
            operand_a, operand_b = self.children
            return op_map[self.node.val](operand_a.eval(), operand_b.eval())

        elif self.node.type_ is TokenType.UNARY_OP and self.node.val == "-":
            return self.children[0].eval() * -1

    def __repr__(self) -> str:
        return f"{self.node} -> {self.children} "
