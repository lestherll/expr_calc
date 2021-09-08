from decimal import Decimal

from expr_calc.token import Token, TokenType
from expr_calc.operators import OP_LIST, op_map, unary_op_map
from expr_calc.errors import NoProgramLoaded, ExcessiveDotError, TokenError

from typing import Optional, List


class Lexer:

    def __init__(self, program: str = "") -> None:
        self.program = program

    @classmethod
    def tokenise(cls, lexeme: str) -> Optional[TokenType]:
        """
        Helper function for mapping lexeme or characters or
        strings into their respective token equivalent

        :param lexeme: lexeme to be mapped to a token type
        :return: TokenType equivalent of the lexeme
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
        """
        Lexes the program given or at self.program. Anything that
        is not a valid token is ignored except for literal dot (.)
        which is used for decimal points

        :param program: optional program to translated into a list of Token objects
        :return:
        """
        if program and not program.isspace():
            self.program = program

        if self.program.isspace() or not self.program:
            raise NoProgramLoaded("No expression loaded\n")

        tokens: List[Token] = []
        program_length = len(self.program)  # will fail if self.program is None as well
        temp_digit = []  # stack for digit chars and decimal sign
        digit_flag = False  # flag when digit is encountered
        dot_flag = False    # flag when dot is encountered

        for i, char in enumerate(self.program):
            token = Lexer.tokenise(char)

            space = " " * i
            if not token and char not in {" ", "."}:
                raise TokenError(f"{self.program}\n"
                                 f"{space}^^^\n"
                                 f"Character {char} is not recognised")

            if token is TokenType.NUMBER:
                temp_digit.append(char)

                # checks if current char which is a number is the last char
                if i + 1 == program_length:
                    tokens.append(Token(TokenType.NUMBER, Decimal("".join(temp_digit))))
                digit_flag = True

            else:

                # current token is not a digit anymore
                if digit_flag:
                    if not dot_flag and char == ".":     # possible decimal point
                        temp_digit.append(char)
                        dot_flag = True
                    elif dot_flag and char == ".":
                        raise ExcessiveDotError("Wrong use of dot for numbers."
                                                " Number can only have 1 dot\n")
                    else:
                        tokens.append(Token(TokenType.NUMBER, Decimal("".join(temp_digit))))
                        temp_digit.clear()
                        digit_flag = False
                        dot_flag = False

                if token is TokenType.BINARY_OP:
                    if char in unary_op_map and (not tokens or tokens[-1].type_ is not TokenType.NUMBER):
                        temp_index = i
                        while temp_index+1 < program_length:
                            if Lexer.tokenise(self.program[temp_index+1]) in\
                                    (TokenType.L_PAREN, TokenType.NUMBER, TokenType.BINARY_OP):
                                tokens.append(Token(TokenType.UNARY_OP, char))
                                break
                            temp_index += 1
                        # temp_digit.append(char)
                    else:
                        tokens.append(Token(TokenType.BINARY_OP, char))

                elif token in (TokenType.L_PAREN, TokenType.R_PAREN):
                    tokens.append(Token(token, char))

        return tokens
