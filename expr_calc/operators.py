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
