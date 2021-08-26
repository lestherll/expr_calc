from typing import List
from calc.calc import Calc, Token, TokenVal

from unittest import TestCase


class TestCalc(TestCase):

    programs = {
        "one_val": "345",
        "basic": "2 3 +",
    }
    
    def test_calc_lex_init(self):
        calc: Calc = Calc(program=TestCalc.programs["basic"])
        calc.lex()

        expected: List[TokenVal] = [
            TokenVal(Token.NUMBER, 2),
            TokenVal(Token.NUMBER, 3),
            TokenVal(Token.BINARY_OP, "+")
        ]

        self.assertListEqual(
            expected, calc.lexed
        )

    def test_calc_lex_not_inplace(self):
        calc: Calc = Calc(program=TestCalc.programs["basic"])
        calc.lex(inplace=False)


        expected: List[TokenVal] = [
            TokenVal(Token.NUMBER, 2),
            TokenVal(Token.NUMBER, 3),
            TokenVal(Token.BINARY_OP, "+")
        ]

        self.assertNotEquals(
            expected, calc.lexed
        )
