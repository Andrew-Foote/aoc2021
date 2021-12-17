import re
from shared import register, main

def parse(ip):
    dots = set()

    for line in ip:
        line = line.strip()

        if not line:
            return dots, list(parse_instructions(ip))

        x, y = line.strip().split(',')
        dots.add((int(x), int(y)))

def parse_instructions(ip):
    for line in ip:
        line = line.strip()

        if line:
            m = re.match(r'fold along ([xy])=(\d+)', line)
            axis, intercept = m.group(1, 2)
            yield ['x', 'y'].index(axis), int(intercept)

    ip.close()

def fold(dots, instruction):
    """
    >>> dots = {(6, 10), (0, 14), (9, 10), (0, 3), (10, 4), (4, 11), (6, 0), (6, 12), (4, 1), (0, 13), (10, 12), (3, 4), (3, 0), (8, 4), (1, 10), (2, 14), (8, 10), (9, 0)}
    >>> print('=' + dotpicture(dots).replace('\\n', '\\n='))
    =...#..#..#.
    =....#......
    =...........
    =#..........
    =...#....#.#
    =...........
    =...........
    =...........
    =...........
    =...........
    =.#....#.##.
    =....#......
    =......#...#
    =#..........
    =#.#........
    >>> new_dots = fold(dots, (1, 7))
    >>> print('=' + dotpicture(new_dots).replace('\\n', '\\n='))
    =#.##..#..#.
    =#...#......
    =......#...#
    =#...#......
    =.#.#..#.###
    """

    axis, intercept = instruction
    new_dots = set()

    for dot in dots:
        if dot[axis] > intercept:
            new_dot = list(dot)
            new_dot[axis] = 2 * intercept - dot[axis]
            new_dots.add(tuple(new_dot))
        else:
            new_dots.add(dot)

    return new_dots

def dotpicture(dots):
    """
    >>> print('=' + dotpicture({(0, 0), (0, 2), (2, 4)}).replace('\\n', '\\n='))
    =#..
    =...
    =#..
    =...
    =..#
    """
    xmax = max(x for x, y in dots)
    ymax = max(y for x, y in dots)
    rows = []

    for y in range(ymax + 1):
        row = []

        for x in range(xmax + 1):
            if (x, y) in dots:
                row.append('#')
            else:
                row.append('.')

        rows.append(''.join(row))

    return '\n'.join(rows)


@register(day=13, level=1)
def level1(ip):
    dots, instructions = parse(ip)
    instruction = instructions[0]
    new_dots = fold(dots, instruction)
    return len(new_dots)

main(__name__)