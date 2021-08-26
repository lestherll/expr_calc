from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, List

OP_LIST = {'+', '-', '*', '/'}


class Token(Enum):
    NUMBER = auto() 
    UNARY_OP = auto()
    BINARY_OP = auto()


@dataclass
class TokenVal:
    token_type: Token
    val: Any

    def __iter__(self):
        return iter((self.token_type, self.val))

class Calc:

    def __init__(self, program: str = None) -> None:
        """
        Initialise a Calc instance/object

        Args:
            program (str, optional): Program to be interpreted. Defaults to None.
        """
        self.program = program
        self.stack = []
        self.lexed = []

        self.op_map = {
            '+': lambda a, b: a + b,
            '*': lambda a, b: a * b,
            '-': lambda a, b: b - a,
            '/': lambda a, b: b / a
        }

    def tokenise(self, lexeme: str) -> Token:
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

    def lex(self) -> List[TokenVal]:
        """
        Lexes the program given
        """
        
        tokens: List[TokenVal] = []

        program_length = len(self.program)

        temp_digit = []
        digit_flag = False
        for i, char in enumerate(self.program):
            token = self.tokenise(char)
            if token is Token.NUMBER:
                digit_flag = True
                temp_digit.append(char)
            else:
                if digit_flag:
                    tokens.append(TokenVal(Token.NUMBER, float("".join(temp_digit))))
                    temp_digit.clear()
                    digit_flag = False
                
                if token is Token.BINARY_OP:
                    tokens.append(TokenVal(Token.BINARY_OP, char))

        self.lexed = tokens
        return tokens

    def eval(self) -> float:
        """
        Iterate through the lexed program and evaluates it

        Returns:
            float: Result of the program
        """
        self.stack.clear()
        if self.program is None:
            print("No program loaded")
            return

        self.program = self.program + " "
        self.lex()

        for type_, val in self.lexed:
            if type_ is Token.NUMBER:
                self.stack.append(val)
            else:
                if type_ is Token.BINARY_OP:
                    if len(self.stack) >= 2:
                        a = self.stack.pop()
                        b = self.stack.pop()
                        res = self.op_map[val](a, b)
                        self.stack.append(res)

        return self.stack[0]

    def repl(self) -> None:
        """
        Runs a REPL which evaluates programs and expressions
        """
        print("WELCOME TO CALCULATOR LANGUAGE!")
        while (program := input("> ")) != "q":
            self.program = program
            print(self.eval(), end="\n\n")




if __name__ == "__main__":
    program = "2 32 + 2 * 12 /"
    calc = Calc()
    # print(calc.eval())
    # calc.repl()

    calc.program = program
    # print(calc.eval())
    calc.repl()