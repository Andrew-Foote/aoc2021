from collections import Counter, defaultdict
from dataclasses import dataclass, field
from shared import register, main, get_input
from utils import common_value

def parse_bits(bits):
    """Parse an iterable of bits into an integer. Most significant first.

    >>> parse_bits([1, 0, 1, 1, 0])
    22
    >>> parse_bits([1, 0, 1, 1, 1])
    23
    >>> parse_bits([0, 1, 0, 1, 0])
    10
    """
    result = 0

    for bit in bits:
        result *= 2
        result += bit

    return result

def parse(ip):
    for line in ip:
        yield (int(c) for c in line.strip())

    ip.close()

@register(day=3, level=1)
def level1(ip):
    """
    >>> level1(get_input(3))
    2743844
    """
    sums = Counter()

    for datum in parse(ip):
        for i, bit in enumerate(datum):
            sums[i] += bit

    gamma_rate = []
    epsilon_rate = []

    for i, _ in enumerate(sums):
        bits = [0, 1]

        # 1 most common
        # (case where sums[i] == 500 is ambiguous)
        if sums[i] > 500:
            bits.reverse()

        most_common, least_common = bits
        gamma_rate.append(most_common)
        epsilon_rate.append(least_common)

    return parse_bits(gamma_rate) * parse_bits(epsilon_rate)

@dataclass
class PrefixTreeWithCounter:
    counter: Counter=field(
        default_factory=lambda: Counter()
    )

    subtrees: defaultdict[int, 'PrefixTree']= field(
        default_factory=lambda: defaultdict(lambda: PrefixTreeWithCounter())
    )

def restructure_data(data):
    """
    >>> data = parse(get_input('3_example'))
    >>> tree = restructure_data(data)
    >>> tree.counter
    Counter({1: 7, 0: 5})
    >>> 1 in tree.subtrees
    True
    >>> tree1 = tree.subtrees[1]
    >>> sorted(tree1.counter.items())
    [(0, 4), (1, 3)]
    >>> 0 in tree1.subtrees
    True
    >>> tree10 = tree1.subtrees[0]
    >>> sorted(tree10.counter.items())
    [(0, 1), (1, 3)]
    >>> 1 in tree10.subtrees
    True
    >>> tree101 = tree10.subtrees[1]
    >>> sorted(tree101.counter.items())
    [(0, 1), (1, 2)]
    >>> 1 in tree101.subtrees
    True
    >>> tree1011 = tree101.subtrees[1]
    >>> sorted(tree1011.counter.items())
    [(0, 1), (1, 1)]
    >>> 1 in tree1011.subtrees
    True
    >>> tree10111 = tree1011.subtrees[1]
    >>> len(tree10111.subtrees)
    0
    """
    tree = PrefixTreeWithCounter()

    for datum in data:
        subtree = tree

        for bit in datum:
            subtree.counter[bit] += 1
            subtree = subtree.subtrees[bit]

    return tree

def life_support_rating_parts(data):
    """
    >>> data = parse(get_input('3_example'))
    >>> life_support_rating_parts(data)
    (23, 10)
    """
    tree = restructure_data(data)
    mcsubtree = tree
    mcbits = []
    lcsubtree = tree
    lcbits = []

    while common_value(*map(bool, (mcsubtree.subtrees, lcsubtree.subtrees))):
        mcbit = (
            1 in mcsubtree.subtrees
            if len(mcsubtree.subtrees) == 1
            else mcsubtree.counter[1] >= mcsubtree.counter[0]
        )

        lcbit = (
            1 in lcsubtree.subtrees
            if len(lcsubtree.subtrees) == 1
            else lcsubtree.counter[1] < lcsubtree.counter[0]
        )

        mcbits.append(mcbit)
        lcbits.append(lcbit)
        mcsubtree = mcsubtree.subtrees[mcbit]
        lcsubtree = lcsubtree.subtrees[lcbit]

    return tuple(map(parse_bits, (mcbits, lcbits)))

@register(day=3, level=2)
def level2(ip):
    oxy_rating, co2_rating = life_support_rating_parts(parse(ip))
    return oxy_rating * co2_rating

main(__name__)