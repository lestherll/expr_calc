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