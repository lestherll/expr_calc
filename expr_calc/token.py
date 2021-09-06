from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """
    Possible TokenTypes for lexemes
    """
    NUMBER = auto()
    UNARY_OP = auto()
    BINARY_OP = auto()
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
