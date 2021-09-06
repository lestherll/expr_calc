import math


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier
    # return math.ceil(n)


OP_LIST = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3
}

op_map = {
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
    '-': lambda a, b: a - b,
    '/': lambda a, b: a / b,
    '^': lambda a, b: a ** b,
    '%': lambda a, b: a % b
}

unary_op_map = {
    '+': lambda a: a,
    '-': lambda a: -a
}
