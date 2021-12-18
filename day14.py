from dataclasses import dataclass
from collections import Counter
import itertools as it
import re
from shared import register, main

@dataclass
class Polymer:
    pair_counter: Counter[str]
    last_letter: str

    @classmethod
    def from_string(cls, s):
        """
        >>> polymer = Polymer.from_string('NNCB')
        >>> {pair: count for pair, count in polymer.pair_counter.items() if count > 0}
        {('N', 'N'): 1, ('N', 'C'): 1, ('C', 'B'): 1}
        >>> polymer.last_letter
        'B'
        """
        pair_counter = Counter(it.pairwise(s))
        last_letter = s[-1]
        return Polymer(pair_counter, last_letter)

    def matches_string(self, s):
        s_counter = Counter(it.pairwise(s))
        return self.pair_counter == s_counter and self.last_letter == s[-1]

    def step(self, rules):
        """
        >>> polymer = Polymer.from_string('NNCB')
        >>> rules = {('C', 'H'): 'B', ('H', 'H'): 'N', ('C', 'B'): 'H', ('N', 'H'): 'C', ('H', 'B'): 'C', ('H', 'C'): 'B', ('H', 'N'): 'C', ('N', 'N'): 'C', ('B', 'H'): 'H', ('N', 'C'): 'B', ('N', 'B'): 'B', ('B', 'N'): 'B', ('B', 'B'): 'N', ('B', 'C'): 'B', ('C', 'C'): 'N', ('C', 'N'): 'C'}
        >>> polymer = polymer.step(rules)
        >>> polymer.matches_string('NCNBCHB')
        True
        >>> polymer = polymer.step(rules)
        >>> polymer.matches_string('NBCCNBBBCBHCB')
        True
        >>> polymer = polymer.step(rules)
        >>> polymer.matches_string('NBBBCNCCNBBNBNBBCHBHHBCHB')
        True
        >>> polymer = polymer.step(rules)
        >>> polymer.matches_string('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
        True
        """
        new_pair_counter = Counter()

        for (left, right), count in self.pair_counter.items():
            if (left, right) in rules:
                between = rules[left, right]
                new_pair_counter[left, between] += count
                new_pair_counter[between, right] += count
            else:
                new_pair_counter[left, right] += count

        return Polymer(new_pair_counter, self.last_letter)

    def steps(self, rules, count):
        polymer = self

        for _ in range(count):
            polymer = polymer.step(rules)

        return polymer

    def letter_counter(self):
        """
        >>> polymer = Polymer.from_string('NNCB')
        >>> rules = {('C', 'H'): 'B', ('H', 'H'): 'N', ('C', 'B'): 'H', ('N', 'H'): 'C', ('H', 'B'): 'C', ('H', 'C'): 'B', ('H', 'N'): 'C', ('N', 'N'): 'C', ('B', 'H'): 'H', ('N', 'C'): 'B', ('N', 'B'): 'B', ('B', 'N'): 'B', ('B', 'B'): 'N', ('B', 'C'): 'B', ('C', 'C'): 'N', ('C', 'N'): 'C'}
        >>> polymer.steps(rules, 10).letter_counter().most_common()
        [('B', 1749), ('N', 865), ('C', 298), ('H', 161)]
        """
        counter = Counter()

        for (letter, _), count in self.pair_counter.items():
            if count > 0:
                counter[letter] += count

        counter[self.last_letter] += 1
        return counter

    def __len__(self):
        """
        >>> polymer = Polymer.from_string('NNCB')
        >>> rules = {('C', 'H'): 'B', ('H', 'H'): 'N', ('C', 'B'): 'H', ('N', 'H'): 'C', ('H', 'B'): 'C', ('H', 'C'): 'B', ('H', 'N'): 'C', ('N', 'N'): 'C', ('B', 'H'): 'H', ('N', 'C'): 'B', ('N', 'B'): 'B', ('B', 'N'): 'B', ('B', 'B'): 'N', ('B', 'C'): 'B', ('C', 'C'): 'N', ('C', 'N'): 'C'}
        >>> len(polymer)
        4
        >>> len(polymer.steps(rules, 5))
        97
        >>> len(polymer.steps(rules, 10))
        3073
        """
        return sum(self.letter_counter().values())

def parse(ip):
    # each letter appears in exactly two pairs, except for the very last one
    template = Polymer.from_string(next(ip).strip())
    rules = {}

    for line in ip:
        line = line.strip()

        if line:
            left, right, between = re.match(r'(\w)(\w) -> (\w)', line).group(1, 2, 3)
            rules[left, right] = between

    ip.close()
    return template, rules

@register(day=14, level=1)
def level1(ip):
    polymer, rules = parse(ip)

    for i in range(10):
        #print({pair: count for pair, count in polymer.pair_counter.items() if count > 0})
        polymer = polymer.step(rules)

    entries = polymer.letter_counter().most_common()
    return entries[0][1] - entries[-1][1]

@register(day=14, level=2)
def level2(ip):
    polymer, rules = parse(ip)

    for i in range(40):
        polymer = polymer.step(rules)

    entries = polymer.letter_counter().most_common()
    return entries[0][1] - entries[-1][1]

main(__name__)