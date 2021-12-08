from collections import Counter
from shared import register, main, get_input
from utils import common_value, sgn

def parse(ip):
    """
    >>> lines = parse(get_input('5_example'))
    >>> next(lines)
    ((0, 9), (5, 9))
    >>> next(lines)
    ((8, 0), (0, 8))
    """
    for line in ip:
        parts = line.strip().split()
        
        start, end = (
            tuple(map(int, p.split(',')))
            for p in (parts[0], parts[2])
        )

        yield start, end

    ip.close()

def is_vertical(start, end):
    return start[0] == end[0]

def is_horizontal(start, end):
    return start[1] == end[1]

def is_diagonal(start, end):
    line = start, end
    return not (is_vertical(*line) or is_horizontal(*line))

def points(start, end):
    """
    >>> list(points((1, 1), (1, 3)))
    [(1, 1), (1, 2), (1, 3)]
    >>> list(points((9, 7), (7, 7)))
    [(9, 7), (8, 7), (7, 7)]
    >>> list(points((1, 1), (3, 3)))
    [(1, 1), (2, 2), (3, 3)]
    >>> list(points((9, 7), (7, 9)))
    [(9, 7), (8, 8), (7, 9)]
    """
    line = start, end

    if is_vertical(*line):
        x = common_value(*(p[0] for p in line))
        y1, y2 = (p[1] for p in line)
        sign = sgn(y2 - y1)

        for y in range(y1, y2 + sign, sign):
            yield x, y

    elif is_horizontal(*line):
        x1, x2 = (p[0] for p in line)
        y = common_value(*(p[1] for p in line))
        sign = sgn(x2 - x1)

        for x in range(x1, x2 + sign, sign):
            yield x, y

    else:
        x1, x2 = (p[0] for p in line)
        y1, y2 = (p[1] for p in line)
        x_sign = sgn(x2 - x1)
        y_sign = sgn(y2 - y1)
        length = common_value(abs(x2 - x1), abs(y2 - y1))

        for i in range(length + 1):
            x = x1 + i * x_sign
            y = y1 + i * y_sign
            yield x, y

def count_overlaps(lines):
    counter = Counter()

    for line in lines:
        for x, y in points(*line):
            counter[x, y] += 1

    return sum(1 for count in counter.values() if count >= 2)

@register(day=5, level=1)
def level1(ip):
    """
    >>> level1(get_input(5))
    3990
    """
    return count_overlaps(line for line in parse(ip) if not is_diagonal(*line))

@register(day=5, level=2)
def level2(ip):
    return count_overlaps(parse(ip))

main(__name__)