from expr_calc.errors import NoProgramLoaded
from enum import Enum, auto
from dataclasses import dataclass

from typing import Any, List, Optional

OP_LIST = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3
}


class TokenType(Enum):
    NUMBER = auto()
    UNARY_OP = auto()
    BINARY_OP = auto()
    L_PAREN = auto()
    R_PAREN = auto()

@dataclass(frozen=True)
class Token:
    type_: TokenType
    val: Any

    def __iter__(self):
        return iter((self.type_, self.val))

    def __repr__(self) -> str:
        return f"{str(self.type_)[10:]}: {self.val}"


class Calc:
    op_map = {
        '+': lambda a, b: a + b,
        '*': lambda a, b: a * b,
        '-': lambda a, b: b - a,
        '/': lambda a, b: b / a,
        '^': lambda a, b: b ** a,
        '%': lambda a, b: b % a
    }

    unary_op_map = {
        '+': lambda a: a,
        '-': lambda a: -a
    }

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
                    if char in Calc.unary_op_map and (not tokens or tokens[-1].type_ is not TokenType.NUMBER):
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

        for token in lexed:

            if token.type_ is TokenType.NUMBER:
                output.append(token)

            elif token.type_ is TokenType.BINARY_OP:
                while operators and operators[-1].val in OP_LIST and OP_LIST[operators[-1].val] >= OP_LIST[token.val]:
                    output.append(operators.pop())
                operators.append(token)

            elif token.type_ is TokenType.UNARY_OP:
                operators.append(token)

            elif token.type_ is TokenType.L_PAREN:
                operators.append(token)

            elif token.type_ is TokenType.R_PAREN:
                while operators and operators[-1].val != "(":
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        self.shunted = list(output)

        return output

    def eval(self, program: str = "", infix: bool = True) -> float:
        """
        Iterate through the lexed program and evaluates it

        Returns:
            float: Result of the program
        """
        if program and not program.isspace():
            self.program = program

        if not self.program or self.program.isspace():
            raise NoProgramLoaded("No program loaded\n")

        self.lex()
        if infix is True:
            self.shunt()
            processed = self.shunted
        else:
            processed = self.lexed

        self.stack.clear()
        unary_minus_flag: bool = False
        for type_, val in processed:
            if type_ is TokenType.NUMBER:
                if unary_minus_flag:
                    self.stack.append(-val)
                else:
                    self.stack.append(val)
            else:
                if type_ is TokenType.BINARY_OP:
                    if len(self.stack) >= 2:
                        a = self.stack.pop()
                        b = self.stack.pop()
                        res = Calc.op_map[val](a, b)
                        self.stack.append(res)
                elif self.stack and type_ is TokenType.UNARY_OP and val == "-":
                    self.stack.append(self.stack.pop() * -1)

        return self.stack[0]

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
