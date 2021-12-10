from collections import Counter
import itertools as it
from shared import register, main
from utils import parse_digits, product

OPENERS = ('(', '[', '{', '<')
CLOSERS = (')', ']', '}', '>')

def closer_for_opener(opener):
	return CLOSERS[OPENERS.index(opener)]

SCORES = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137
}

def discard_corrupted(lines):
	counter = Counter()

	for line in lines:
		opener_stack = []

		for c in line.strip():
			if c in OPENERS:
					opener_stack.append(c)
			elif c in CLOSERS:
				opener = opener_stack.pop()
				expected_closer = closer_for_opener(opener)

				if c != expected_closer:
					counter[c] += 1
					break
			else:
				assert False
		else:
			yield line, opener_stack

	return counter

@register(day=10, level=1)
def level1(ip):
	counter = yield from discard_corrupted(ip)
	return sum(SCORES[closer] * count for closer, count in counter.items())

@register(day=10, level=2)
def level2(ip):
	scores = []

	for line, opener_stack in discard_corrupted(ip):
		opener_stack.reverse()
		closers = map(closer_for_opener, opener_stack)
		
		score = parse_digits(
			(CLOSERS.index(closer) + 1 for closer in closers),
			5
		)

		scores.append(score)

	scores.sort()
	return scores[len(scores) // 2]

main(__name__)