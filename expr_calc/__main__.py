from expr_calc.calc import Calc
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter flags")
    parser.add_argument(
        "--postfix",
        dest="mode",
        action="store_const",
        const=True,
        default=False,
        help="Use postfix mode (default: False)"
    )
    args = parser.parse_args()

    calculator: Calc = Calc()
    calculator.repl()
