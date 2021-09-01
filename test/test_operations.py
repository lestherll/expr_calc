import pytest

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
    assert result == calc.eval()


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
    assert result == calc.eval()