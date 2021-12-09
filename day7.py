from shared import register, main, get_input

def parse(ip):
	return sorted(map(int, next(ip).split(',')))
	ip.close()

def cheapest(positions):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> cheapest(positions)
	2
	"""
	return positions[len(positions) // 2]

def cost(positions, target):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> target = cheapest(positions)
	>>> cost(positions, target)
	37
	"""
	return sum(abs(position - target) for position in positions)

@register(day=7, level=1)
def level1(ip):
	positions = parse(ip)
	target = cheapest(positions)
	return cost(positions, target)

main(__name__)