import functools as ft
import itertools as it
import operator

def common_value(first, *rest):
	assert all(i == first for i in rest)
	return first

def fiter(f, n, x):
    y = x

    for _ in range(n):
        y = f(y)

    return y

def sgn(x):
	return x // abs(x)

def product(iterable):
    """
    >>> product((1, 2, 3, 4))
    24
    """
    return ft.reduce(operator.mul, iterable, 1)

def parse_digits(digits, base):
    """Parse an iterable of digits into an integer. Most significant first.

    >>> parse_digits([1, 0, 1, 1, 0], 2)
    22
    >>> parse_digits([1, 0, 1, 1, 1], 2)
    23
    >>> parse_digits([0, 1, 0, 1, 0], 2)
    10
    >>> parse_digits([1, 2, 3], 10)
    123
    >>> parse_digits([15, 15, 15, 15], 16)
    65535
    """
    result = 0

    for digit in digits:
        result *= base
        result += digit

    return result

parse_bits = ft.partial(parse_digits, base=2)

def digits(n, base, length=None):
    """
    >>> digits(123, 10)
    [1, 2, 3]
    >>> digits(0b11010111, 2)
    [1, 1, 0, 1, 0, 1, 1, 1]
    >>> digits(0xf, 2, 8)
    [0, 0, 0, 0, 1, 1, 1, 1]
    """
    digits = []

    for i in it.count():
        if (length is None and not n) or (length is not None and i >= length):
            break

        digits.append(n % base)
        n //= base

    digits.reverse()
    return digits

if __name__ == '__main__':
    import doctest
    doctest.testmod()