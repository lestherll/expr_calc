from .calc import Calc
from .shunting import shunt

if __name__ == "__main__":
    calculator: Calc = Calc()
    calculator.repl()
