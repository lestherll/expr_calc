import pytest

from expr_calc.calc import Calc
from expr_calc.token import Token, TokenType


@pytest.mark.parametrize("source, expected_tokens", [
    ("345", [Token(TokenType.NUMBER, 345)]),
    ("2 3 +", [
        Token(TokenType.NUMBER, 2),
        Token(TokenType.NUMBER, 3),
        Token(TokenType.B_ADD, "+")
    ]),
    ("-2 * -1", [
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.B_MUL, "*"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 1)
    ]),
    ("-1^2", [
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 1),
        Token(TokenType.B_EXP, "^"),
        Token(TokenType.NUMBER, 2)
    ]),
    ("-345^2+-1", [
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 345),
        Token(TokenType.B_EXP, "^"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.B_ADD, "+"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 1)
    ]),
    ("1---+---2^-((+2))", [
        Token(TokenType.NUMBER, 1),
        Token(TokenType.B_MIN, "-"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.U_ADD, "+"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.B_EXP, "^"),
        Token(TokenType.U_MIN, "-"),
        Token(TokenType.L_PAREN, "("),
        Token(TokenType.L_PAREN, "("),
        Token(TokenType.U_ADD, "+"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.R_PAREN, ")"),
        Token(TokenType.R_PAREN, ")")
    ])
])
def test_lex(source, expected_tokens):
    calc: Calc = Calc()
    assert calc.lex(source) == expected_tokens
