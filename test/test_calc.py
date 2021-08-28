from dataclasses import dataclass
from typing import List
from calc.calc import Calc, Token, TokenVal

import pytest


@dataclass(frozen=True)
class MockProgram:
    """Contains source code and tokens of the source in a program"""
    source: str
    token: List[TokenVal]


@pytest.fixture
def programs():
    return {
        "one_val": MockProgram(
            "345",
            [TokenVal(Token.NUMBER, 345)]
        ),
        "basic": MockProgram(
            "2 3 +",
            [
                TokenVal(Token.NUMBER, 2),
                TokenVal(Token.NUMBER, 3),
                TokenVal(Token.BINARY_OP, "+")
            ]
        )
    }


def test_calc_lex_init(programs):
    """Test if program is loaded"""
    calc: Calc = Calc(program=programs["basic"].source)
    assert programs["basic"].source == calc.program


def test_calc_lex(programs):
    calc: Calc = Calc(program=programs["basic"].source)
    actual_tokens: List[TokenVal] = calc.lex()

    assert programs["basic"].token == actual_tokens
    assert programs["basic"].token == calc.lexed


def test_calc_lex_external(programs):
    """"""
    calc: Calc = Calc()
    calc.lex(program=programs["basic"].source)

    assert programs["basic"].source == calc.program
    assert programs["basic"].token == calc.lexed
