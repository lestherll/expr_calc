from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """
    Possible TokenTypes for lexemes
    """
    # literals
    NUMBER = auto()

    # binary operator tokens
    B_ADD = auto()
    B_MIN = auto()
    B_MUL = auto()
    B_DIV = auto()
    B_EXP = auto()
    B_MOD = auto()

    # unary operator tokens
    U_ADD = auto()
    U_MIN = auto()

    # parenthesis
    L_PAREN = auto()
    R_PAREN = auto()


@dataclass(frozen=True)
class Token:
    """
    Token that contains the token type and the value of a lexeme
    """
    type_: TokenType
    val: Any

    def __iter__(self):
        return iter((self.type_, self.val))

    def __repr__(self) -> str:
        return f"{str(self.type_)[10:]}: {self.val}"


B_OP_TOKENS = {TokenType.B_EXP, TokenType.B_MIN, TokenType.B_ADD,
               TokenType.B_DIV, TokenType.B_MUL, TokenType.B_MOD}