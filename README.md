# Calc Interpreter
A mini-language modeled after a calculator implemented in Python 3.
The program currently only lexes basic mathematical expressions. It
supports infix (*using Shunting Yard Algorithm*) and postfix 
(*Reverse Polish Notation*).

## Usage
The best way to run the program currently is to execute the REPL and
can be done in a python file or through your terminal.

Assuming your present working directory is inside the cloned repo, you
can run the following command without the comment.
```shell
# inside /clone_path/calc/
python -m calc
```

## Features
- Infix expressions
- Postfix expressions
- Basic operators such as `+, -, *, /, %, ^`
- Tokens created from an expression can also be fetched if one wanted to do so