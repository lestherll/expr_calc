# Calc Interpreter
[![Python Package](https://github.com/lestherll/calc/actions/workflows/main.yml/badge.svg)](https://github.com/lestherll/calc/actions/workflows/main.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/expr-calc?style=plastic)](https://pypi.org/project/expr-calc/)
[![Python Implementation](https://img.shields.io/pypi/implementation/expr-calc?style=plastic&color=green)](https://python.org/downloads)

A mini-language modeled after a calculator implemented in Python 3.
The program currently only lexes basic mathematical expressions. It
supports infix (*using Shunting Yard Algorithm*) and postfix 
(*Reverse Polish Notation*).

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

Enabling postfix expression mode is also possible. Using infix expressions
in postfix mode is currently undefined and so is using postfix expressions
in infix mode.
```shell
python -m expr_calc --postfix
```

## Features
- Infix expressions
- Postfix expressions
- Basic operators such as `+, -, *, /, %, ^`
- Tokens created from an expression can also be fetched if one wanted to do so
