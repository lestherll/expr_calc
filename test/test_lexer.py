import pytest

from expr_calc.calc import Token, TokenType, Calc


@pytest.mark.parametrize("source, expected_tokens", [
    ("345", [Token(TokenType.NUMBER, 345)]),
    ("2 3 +", [
        Token(TokenType.NUMBER, 2),
        Token(TokenType.NUMBER, 3),
        Token(TokenType.BINARY_OP, "+")
    ]),
    ("-2 * -1", [
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.BINARY_OP, "*"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 1)
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
    ]),
    ("1---+---2^-((+2))", [
        Token(TokenType.NUMBER, 1),
        Token(TokenType.BINARY_OP, "-"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.UNARY_OP, "+"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.L_PAREN, "("),
        Token(TokenType.L_PAREN, "("),
        Token(TokenType.UNARY_OP, "+"),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.R_PAREN, ")"),
        Token(TokenType.R_PAREN, ")")
    ])
])
def test_lex(source, expected_tokens):
    calc: Calc = Calc()
    assert expected_tokens == calc.lex(source)
