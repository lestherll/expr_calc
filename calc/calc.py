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


class Token(Enum):
    NUMBER = auto()
    UNARY_OP = auto()
    BINARY_OP = auto()
    L_PAREN = auto()
    R_PAREN = auto()


@dataclass(frozen=True)
class TokenVal:
    type_: Token
    val: Any

    def __iter__(self):
        return iter((self.type_, self.val))


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

    def __init__(self, program: str = None) -> None:
        """
        Initialise a Calc instance/object

        Args:
            program (str, optional): Program to be interpreted. Defaults to None.
        """
        self.program = program
        self.stack = []

        self.lexed = []
        self.shunted = []

    def tokenise(self, lexeme: str) -> Optional[Token]:
        """
        Helper function for mapping lexeme or characters or
        strings into their respective token equivalent

        Args:
            lexeme (str): string to be mapped to token

        Returns:
            Token: resulting token of the lexeme
        """
        if lexeme.isdigit():
            return Token.NUMBER
        elif lexeme in OP_LIST:
            return Token.BINARY_OP
        elif lexeme == "(":
            return Token.L_PAREN
        elif lexeme == ")":
            return Token.R_PAREN

    def lex(self, program: str = None) -> List[TokenVal]:
        """Lexes the program given or at self.program

        Args:
            program (str, optional): Optional program. Defaults to None.

        Returns:
            List[TokenVal]: [description]
        """

        if program is not None:
            self.program = program

        tokens: List[TokenVal] = []
        program_length = len(self.program)  # will fail if self.program is None as well
        temp_digit = []  # stack for digit chars and decimal sign
        digit_flag = False  # flag when digit is encountered

        for i, char in enumerate(self.program):
            token = self.tokenise(char)
            if token is Token.NUMBER:
                temp_digit.append(char)

                # checks if current char which is a number is the last char
                if i + 1 == program_length:
                    tokens.append(TokenVal(Token.NUMBER, float("".join(temp_digit))))
                digit_flag = True

            else:
                if digit_flag:
                    if char == ".":
                        temp_digit.append(char)
                    else:
                        tokens.append(TokenVal(Token.NUMBER, float("".join(temp_digit))))
                        temp_digit.clear()
                        digit_flag = False

                if token is Token.BINARY_OP:
                    if i < program_length and char in Calc.unary_op_map and \
                            (not tokens or tokens[-1].type_ is not Token.NUMBER) and \
                            self.tokenise(self.program[i + 1]) is Token.NUMBER:
                        temp_digit.append(char)
                    else:
                        tokens.append(TokenVal(Token.BINARY_OP, char))

                if token in (Token.L_PAREN, Token.R_PAREN):
                    tokens.append(TokenVal(token, char))

        self.lexed = tokens  # update self.lexed

        return tokens

    def shunt(self, program: str = None) -> List[TokenVal]:
        """Uses the result of the lexer to generate
        expressions from infix to postfix

        Args:
            program (str, optional): program to be evaluated. Defaults to None.

        Returns:
            List: [description]
        """

        if program is not None:
            lexed = self.lex(program=program)
        else:
            lexed = self.lex()

        operators = []
        output = []

        for token in lexed:

            if token.type_ is Token.NUMBER:
                output.append(token)

            elif token.type_ is Token.BINARY_OP:
                while operators and operators[-1].val in OP_LIST and OP_LIST[operators[-1].val] >= OP_LIST[token.val]:
                    output.append(operators.pop())
                operators.append(token)

            elif token.type_ is Token.L_PAREN:
                operators.append(token)

            elif token.type_ is Token.R_PAREN:
                while operators and operators[-1].val != "(":
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        self.shunted = list(output)

        return output

    def eval(self, infix: bool = True) -> float:
        """
        Iterate through the lexed program and evaluates it

        Returns:
            float: Result of the program
        """

        self.stack.clear()

        if self.program is None:
            raise ValueError("No program loaded")

        self.lex()
        if infix is True:
            self.shunt()
            processed = self.shunted
        else:
            processed = self.lexed

        for type_, val in processed:
            if type_ is Token.NUMBER:
                self.stack.append(val)
            else:
                if type_ is Token.BINARY_OP:
                    if len(self.stack) >= 2:
                        a = self.stack.pop()
                        b = self.stack.pop()
                        res = Calc.op_map[val](a, b)
                        self.stack.append(res)

                    # elif len(self.stack) == 1 and val in "-+":
                    #     self.stack.append(Calc.unary_op_map[val](self.stack.pop()))

        return self.stack[0]

    def repl(self, infix=True) -> None:
        """
        Runs a REPL which evaluates programs and expressions
        """
        print("WELCOME TO CALCULATOR LANGUAGE!")
        while (program := input("> ")) != "q":
            self.program = program
            print(self.eval(infix=infix), end="\n\n")
