from dataclasses import dataclass
from collections import Counter
import itertools as it
import re
from shared import register, main

def repstring_append_with_count(s, c, count):
    if len(s) > 0 and s[-1][0] == c:
        letter, prevcount = s[-1]
        s[-1] = (letter, prevcount + count)
    else:
        s.append((c, count))

def repstring_append(s, c):
    return repstring_append_with_count(s, c, 1)

def repstring(s):
    result = []

    for c in s:
        repstring_append(result, c)

    return result

def parse(ip):
    template = repstring(next(ip).strip())
    rules = {}

    for line in ip:
        line = line.strip()

        if line:
            left, right, between = re.match(r'(\w)(\w) -> (\w)', line).group(1, 2, 3)
            rules[left, right] = between

    ip.close()
    return template, rules

def step(template, rules):
    """
    >>> tuple(step([['N', 2], ['C', 1], ['B', 1]], {('N', 'N'): 'C', ('N', 'C'): 'B', ('C', 'B'): 'H'}))
    (('N', 1), ('C', 1), ('N', 1), ('B', 1), ('C', 1), ('H', 1), ('B', 1))
    """
    polymer = []

    for (left, lc), (right, rc) in it.pairwise(template):
        if (left, left) in rules:
            for _ in range(lc - 1):
                repstring_append(polymer, left)
                repstring_append(polymer, rules[left, left])

            repstring_append(polymer, left)
        else:
            repstring_append_with_count(polymer, left, lc)

        if (left, right) in rules:
            repstring_append(polymer, rules[left, right])

    repstring_append_with_count(polymer, *template[-1])
    return polymer

@register(day=14, level=1)
def level1(ip):
    template, rules = parse(ip)

    for i in range(10):
        template = step(template, rules)
        print(f'{i} | {template}')

    counter = Counter({letter: count for letter, count in template})
    print(counter)
    entries = counter.most_common()
    print(entries)
    return entries[0][1] - entries[-1][1]

@register(day=14, level=2)
def level2(ip):
    template, rules = parse(ip)
    print(f'template: {template}')

    for _ in range(40):
        template = step(template, rules)

    counter = Counter({letter: count for letter, count in template})
    entries = counter.most_common()
    print(entries)
    return entries[0][1] - entries[-1][1]

main(__name__)