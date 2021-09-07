from decimal import Decimal


def add(a: Decimal, b: Decimal) -> Decimal:
    """Add b to a"""
    return a + b


def sub(a: Decimal, b: Decimal) -> Decimal:
    """Subtract b from a"""
    return a - b


def mul(a: Decimal, b: Decimal) -> Decimal:
    """Multiply a by b"""
    return a * b


def div(a: Decimal, b: Decimal) -> Decimal:
    """Divide a into b"""
    return a / b


def exp(a: Decimal, b: Decimal) -> Decimal:
    """Raise a to b"""
    return a ** b


def mod(a: Decimal, b: Decimal) -> Decimal:
    """Get the remainder of the true division of a into b"""
    return a % b


def identity(a: Decimal) -> Decimal:
    """Return itself"""
    return a


def negative(a: Decimal) -> Decimal:
    """Return the negative of a"""
    return -a


OP_LIST = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3
}

op_map = {
    '+': add,
    '*': mul,
    '-': sub,
    '/': div,
    '^': exp,
    '%': mod
}

unary_op_map = {
    '+': identity,
    '-': negative
}