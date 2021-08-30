from expr_calc.calc import Calc


def test_calc_init():
    """Test if program is loaded"""
    calc: Calc = Calc("1 + 1")
    assert "1 + 1" == calc.program
