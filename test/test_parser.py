import pytest

from calc.calc import Token, TokenType, Calc


@pytest.mark.parametrize("source, expected_shunted_tokens", [
    ("1 + 1", [
        Token(TokenType.NUMBER, 1),
        Token(TokenType.NUMBER, 1),
        Token(TokenType.BINARY_OP, "+")
    ]),
    ("-10 ^ 2", [
        Token(TokenType.NUMBER, 10),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.UNARY_OP, "-")
    ]),
    ("-1 ^ -2", [
        Token(TokenType.NUMBER, 1),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.UNARY_OP, "-"),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.UNARY_OP, "-")
    ]),
    ("-2 ^ 2/3", [
        Token(TokenType.NUMBER, 2),
        Token(TokenType.NUMBER, 2),
        Token(TokenType.BINARY_OP, "^"),
        Token(TokenType.NUMBER, 3),
        Token(TokenType.BINARY_OP, "/"),
        Token(TokenType.UNARY_OP, "-")
    ])
])
def test_shunt(source, expected_shunted_tokens):
    calc: Calc = Calc()
    assert expected_shunted_tokens == calc.shunt(source)