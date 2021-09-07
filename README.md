# Calc Interpreter
[![Python Package](https://github.com/lestherll/calc/actions/workflows/main.yml/badge.svg)](https://github.com/lestherll/calc/actions/workflows/main.yml)
[![other branches](https://github.com/lestherll/expr_calc/actions/workflows/test_other_branch.yml/badge.svg?branch=arbitrary-precision)](https://github.com/lestherll/expr_calc/actions/workflows/test_other_branch.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/expr-calc?style=plastic)](https://pypi.org/project/expr-calc/)
[![Python Implementation](https://img.shields.io/pypi/implementation/expr-calc?style=plastic&color=green)](https://python.org/downloads)

An interpreter modeled after a calculator implemented in Python 3.
The program currently only supports basic mathematical expressions.
The package uses Reverse Polish Notation also known as postfix expression
internally to easily represent mathematical expressions. This is powerful
as it allows operators to be *organised* in such a way that precedence
is *absolute* meaning an operator that is encountered first will always
be executed first.

However, it is obvious that postfix is not *normal* or rather not usually 
taught in schools and thus infix expression is still the way for the user 
to write expressions. The interpreter uses a modified Shunting-Yard algorithm
to produce Abstract Syntax Trees. Evaluation of ASTs is trivial, and they are
flexible making it easy to extend the grammar and functionality later on.

## Installation
The package is available in PyPI and can be installed via pip.
```shell
pip install expr-calc
#or
python3 -m pip install expr-calc
```

## Usage 
The best way to run the program currently is to execute the REPL and
can be done in a python file or through your terminal.

Assuming your present working directory is inside the cloned repo, you
can run the following command without the comment.
```shell
# inside /clone_path/expr_calc/
python -m expr_calc
```
The test suite can also be ran with `pytest` when inside the cloned repo
```shell
pytest  # or python -m pytest
```

## Example
Once inside the REPL, you can start evaluating expressions. Currently, 
only operators listed in [Features](#features) are supported.
```shell
calc> 1 + 1
2

calc> 345--500
845

calc> -2
-2

calc> 123 ^ 4
228886641

calc> 32 / 1.5
21.33333333333333333333333333

calc> 123 * 456
56088

calc> 34 % 5
4

calc> 4 ^ 1/2
0.5

calc> 4 ^ (1/2)
2.0
```

## Features
- Infix expressions
- Basic operators such as `+, -, *, /, %, ^`
- Tokens created from an expression can also be fetched to be manipulated if one wanted to do so
- Expressions are transformed into m-ary Tree objects connected to each other

### Features I want to add later
- variable support
- custom functions
- more mathematical functions such as `sin`, `cos`, `tan`, etc
- and possibly a simple symbolic computation support

## Resources
- [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
- [Shunting Yard Algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm)
- [Floating-point arithmetic](https://floating-point-gui.de/formats/fp/)
- [Calculator test suite](https://mozilla.github.io/calculator/test/)

