import pytest
import math

from expr_calc.calc import Calc


@pytest.mark.parametrize("expression, result", [
    ("1 + 1", 2),
    ("-1 + 5", 4),
    ("3.4 + 56", 59.4),
    ("1.5 + 1.5", 3.0),
    ("-12 + 0", -12),
    ("0 + 459", 459),
    ("-34 + 35", 1),
    ("99999999 + 99999999", 199999998),
    ("-100.43  + 200", 99.57),
    # TODO: add positive integer to result of previous eval
    # TODO: add positive float to result of previous eval
    # TODO: add floating point number with many decimals places to previous eval
    # TODO: add large integer to previous eval
])
def test_add(expression, result):
    calc: Calc = Calc(expression)
    assert calc.eval() == result


@pytest.mark.parametrize("expression, result", [
    ("1 - 1", 0),
    ("0 - 53", -53),
    ("5 - 0", 5),
    ("-10 - 3.4", -13.4),
    ("1.5 - 10", -8.5),
    ("230 + -10.3", 219.7),
    ("100.5 - 200.5", -100.0),
    ("7.1234567 - 2.2109876", 4.9124691),
    ("1000 - -10.98", 1010.98),
    ("-2.01 + -97.99", -100.0),
    ("-34 + 35", 1),
    ("50 + -60", -10),
    ("-10 + -100", -110),
    ("-1.5 - 100", -101.5),
    ("123456789 - 210987654", -87530865),
    ("7.12345678 - 2.21098765", 4.91246913)
    # TODO: subtract integer form previous eval
    # TODO: subtract floating point from form previous eval
    # TODO: subtract large floating point num from previous eval
    # TODO: subtract large integer from previous eval
])
def test_sub(expression, result):
    calc: Calc = Calc(expression)
    assert calc.eval() == result


@pytest.mark.parametrize("expression, result", [
    ("9 * 9", 81),
    ("0.5 * 10", 5),
    ("5 * 1.23", 6.15),
    ("5.23 * 6.46", 33.7858),
    ("999 * 0", 0),
    ("-999 * 23", -22977),
    ("-123.45 * 10", -1234.5),
    # TODO: floating point errors
    ("-456.78 * 2.3", -1050.594),
    ("1.23456789 * 2.10987654", 2.6047858281),
    ("99999999 * 99999999", 9999999800000001),
    # TODO: multiply the result of a previous eval by a positive floating point number‣
    # TODO: multiply the result of a previous eval by a positive integer‣
    # TODO: multiply the result of a previous eval by large integer‣
    # TODO: multiply the result of a previous eval by a many digit floating point number‣
    # TODO: multiply result of a previous eval when the previous result is zero  
])
def test_multiplication(expression, result):
    calc: Calc = Calc(expression)
    assert calc.eval() == result


@pytest.mark.parametrize("expression, result", [
    ("6 / 2", 3),
    ("0 / 123", 0),
    ("-1500 / 2000", -0.75),
    ("-3.123 / 5", -0.6246),
    ("-5 / 3.123", -1.60102466),
    ("4.21 / 3", 1.40333333),
    ("10 / 3.123", 3.20204931),
    ("0.234 / 3.123", 0.0749279539),
    ("1.23456789 / 2.10987654", 0.585137503)
    # TODO: divide the result of a previous operation by a positive floating point number‣
    # TODO: divide the result of a previous operation by a positive integer‣
    # TODO: report error for division by 0‣
    # TODO: divide two many digit floating point numbers‣
    # TODO: to divide the result of a previous operation by a many digit floating point number‣
    # TODO: divide the result of a previous operation by a large integer
])
def test_division(expression, result):
    calc: Calc = Calc(expression)
    assert calc.eval() == result
