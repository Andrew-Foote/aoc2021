from collections import Counter
import itertools as it
from shared import register, main
from utils import product

OPENERS = ('(', '[', '{', '<')
CLOSERS = (')', ']', '}', '>')

SCORES = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137
}

@register(day=10, level=1)
def level1(ip):
	counter = Counter()

	for line in ip:
		opener_stack = []

		for c in line:
			if c in OPENERS:
				opener_stack.append(c)
			elif c in CLOSERS:
				opener = opener_stack.pop()

				if opener != c:
					counter[c] += 1
					break
			else:
				assert False

	print(counter)

	return sum(SCORES[closer] * count for closer, count in counter.items())


main(__name__)