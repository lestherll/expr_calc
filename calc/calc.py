from enum import Enum, auto
from dataclasses import dataclass
from collections import deque
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
            '/': lambda a, b: b / a,
            '^': lambda a, b: b ** a,
            '%': lambda a, b: b % a
        }

        if program is not None:
            self.lex()
            

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

    def lex(self, program: str = None, inplace: bool = True) -> List[TokenVal]:
        """
        Lexes the program given
        """

        if program is not None and inplace:
            program_to_use = program
            self.program = program
        else:
            program_to_use = self.program

        tokens: List[TokenVal] = []
        program_length = len(program_to_use)
        temp_digit = []
        digit_flag = False
        for i, char in enumerate(program_to_use):
            token = self.tokenise(char)
            if token is Token.NUMBER:
                temp_digit.append(char)

                # checks if current char which is a number is the last char
                if i+1 == program_length:
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
                    tokens.append(TokenVal(Token.BINARY_OP, char))

                if token in (Token.L_PAREN, Token.R_PAREN):
                    tokens.append(TokenVal(token, char)) 

        if inplace:
            self.lexed = tokens

        return tokens

    def shunt(self, program: str = None, inplace: bool = True) -> List:
        """Uses the result of the lexer to generate 
        expressions from infix to postfix

        Args:
            program (str, optional): program to be evaluated. Defaults to None.
            inplace (bool, optional): flag to check whether to modify self.shunted or not. Defaults to True.

        Returns:
            List: [description]
        """
        
        if program is None:
            lexed = self.lex()
        else:
            lexed = self.lex(program=program)
        
        operators = []
        output = deque()

        for token in lexed:

            if token.type_ is Token.NUMBER:
                output.append(token)

            elif token.type_ is Token.BINARY_OP:
                while operators and operators[-1].type_ in OP_LIST and OP_LIST[operators[-1].val] > OP_LIST[token.val]:
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

        if inplace:
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
            print("No program loaded")
            return

        self.lex(inplace=True)
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
                        res = self.op_map[val](a, b)
                        self.stack.append(res)

        return self.stack[0]

    def repl(self, infix=True) -> None:
        """
        Runs a REPL which evaluates programs and expressions
        """
        print("WELCOME TO CALCULATOR LANGUAGE!")
        while (program := input("> ")) != "q":
            self.program = program
            print(self.eval(infix=True), end="\n\n")
