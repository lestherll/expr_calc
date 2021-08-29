from calc.calc import Calc, TokenType, Token

import pytest


def test_calc_init():
    """Test if program is loaded"""
    calc: Calc = Calc("1 + 1")
    assert "1 + 1" == calc.program


@pytest.mark.parametrize("source, expected_tokens", [
    ("345", [Token(TokenType.NUMBER, 345)]),
    ("2 3 +", [
        Token(TokenType.NUMBER, 2),
        Token(TokenType.NUMBER, 3),
        Token(TokenType.BINARY_OP, "+")
    ]),
    ("-1^2", [
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 1),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.NUMBER, 2)
    ]),
    ("-345^2+-1", [
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 345),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.BINARY_OP, "+"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 1)
    ])
])
def test_lex(source, expected_tokens):
    calc: Calc = Calc()
    assert expected_tokens == calc.lex(source)
