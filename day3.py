from collections import Counter
from dataclasses import dataclass
from shared import register, main
from utils import common_value

def parse(ip):
	for line in ip:
		yield (int(c) for c in enumerate(line.strip()))

	ip.close()

@register(day=3, level=1)
def level1(ip):
	sums = Counter()

	for datum in parse(ip):
		for i, bit in enumerate(datum):
			sums[i] += bit

	gamma_rate = []
	epsilon_rate = []

	for i, _ in enumerate(sums):
		bits = ['0', '1']

		# 1 most common
		# (case where sums[i] == 500 is ambiguous)
		if sums[i] > 500:
			bits.reverse()

		most_common, least_common = bits
		gamma_rate.append(most_common)
		epsilon_rate.append(least_common)

	gamma_rate = ''.join(gamma_rate)
	epsilon_rate = ''.join(epsilon_rate)
	return int(gamma_rate, 2) * int(epsilon_rate, 2)

@dataclass
class PrefixTree:
	sum_: int # number of 1 bits at the position
 	subtrees: defaultdict[int, PrefixTree]=defaultdict(lambda: PrefixTree())

@register(day=3, level=2)
def level2(ip):
	prefix_tree = new_prefix_tree()
	length = 0

	for datum in parse(ip):
		subtree = prefix_tree

		for bit in datum:
			subtree.sum_ += bit
			subtree = subtree.subtrees[bit]

		length += 1

	def oxygen_generator_rating():
		subtree = prefix_tree
		bits = []

		while subtree.subtrees:
			bit = (
				1 in subtree.subtrees
				if len(subtree.subtrees) == 1
				else subtree.sum_ >= 500
			)

			bits.append(bit)
			subtree = subtree.subtrees[bit]

		return int(''.join(bits), 2)

	mcsubtree = prefix_tree
	mcbits = []
	lcsubtree = prefix_tree
	lcbits = []

	while common_value(*map(bool, (mcsubtree.subtrees, lcsubtree.subtrees))):
		mcbit = (
			1 in mcsubtree
			if len(mcsubtree.subtrees) == 1
			else mcsubtree._sum >= 500
		)

		lcbit = (
			1 in lcsubtree
			if len(lcsubtree.subtrees) == 1
			else lcsubtree._sum < 500
		)

		mcbits.append(mcbit)
		lcbits.append(lcbit)
		mcsubtree = mcsubtree.subtrees[mcbit]
		lcsubtree = lcsubtree.subtrees[lcbit]

	oxy_rating, co2_rating = (int(''.join(bits), 2) for bits in (mcbits, lcbits))
	return oxy_rating * co2_rating

main(__name__)