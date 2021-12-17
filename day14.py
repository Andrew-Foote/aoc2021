from collections import Counter
import itertools as it
import re
from shared import register, main

def parse(ip):
    template = next(ip)
    rules = {}

    for line in ip:
        line = line.strip()

        if line:
            left, right, between = re.match(r'(\w)(\w) -> (\w)', line).group(1, 2, 3)
            rules[left, right] = between

    ip.close()
    return template, rules

def step(template, rules):
    polymer = []

    for left, right in it.pairwise(template):
        polymer.append(left)

        if (left, right) in rules:
            polymer.append(rules[left, right])

    polymer.append(template[-1])
    return polymer

@register(day=14, level=1)
def level1(ip):
    template, rules = parse(ip)

    for _ in range(10):
        template = step(template, rules)

    counter = Counter(template)
    entries = counter.most_common()
    return entries[0][1] - entries[-1][1]

main(__name__)