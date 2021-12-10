import functools as ft

def common_value(first, *rest):
	assert all(i == first for i in rest)
	return first

def sgn(x):
	return x // abs(x)

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