import itertools as it
from shared import register, main

@register(day=1, level=1)
def level1(ip):
	return sum(prv < nxt for prv, nxt in it.pairwise(map(int, ip)))

def triplewise(iterable):
	"""
	>>> list(triplewise([1, 2, 3, 4, 5]))
	[(1, 2, 3), (2, 3, 4), (3, 4, 5)]
	"""
	a, b, c = it.tee(iterable, 3)
	next(b, None)
	next(c, None)
	next(c, None)
	return zip(a, b, c)

@register(day=1, level=2)
def level2(ip):
	return sum(prv < nxt for prv, nxt in it.pairwise(
		map(sum, triplewise(
			map(int, ip)
		))
	))

main(__name__)