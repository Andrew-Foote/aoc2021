from shared import register, main, get_input

def parse(ip):
	return sorted(map(int, next(ip).split(',')))
	ip.close()

def cheapest_level1(positions):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> cheapest_level1(positions)
	2
	"""

	# for each position x, the cost of aligning on that
	# position is sum_i |x_i - x|
	# hence the cheapest one is the one that minimizes that
	# i'm not sure how we get from that to the median though

	return positions[len(positions) // 2]

def cheapest_level2(positions):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> cheapest_level2(positions)
	5
	"""

	# with the new fuel rules, cost of alignment is now
	# sum_i (1 + 2 + ... + |x_i - x|) 
	# = sum_i |x_i - x|(|x_i - x| + 1)/2
	# = sum_i [(x_i - x)^2/2 + |x_i - x|/2]
	# = sum_i (x_i - x)^2/2 + sum_i |x_i - x|/2
	# and i feel like that should be the mean... but can't prove it

	#return round(sum(positions) / len(positions))

	# indeed, it appears it's not (always) the mean (though it works for the example)
	# we could just brute force it instead
	# although we do have to include all the positions in between the given ones

	min_cost = None
	position = None

	for target in range(min(positions), max(positions) + 1):
		cost = cost_level2(positions, target)
		if min_cost is None or cost < min_cost:
			min_cost = cost
			position = target

	return position

def cost_level1(positions, target):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> cost_level1(positions, 2)
	37
	"""
	return sum(abs(position - target) for position in positions)

def cost_level2(positions, target):
	"""
	>>> positions = parse(get_input('7_example'))
	>>> cost_level2(positions, 5)
	168
	>>> cost_level2(positions, 2)
	206
	"""
	cost = 0

	for position in positions:
		d = abs(position - target)
		cost += d * (d + 1) // 2

	return cost

@register(day=7, level=1)
def level1(ip):
	positions = parse(ip)
	target = cheapest_level1(positions)
	return cost_level1(positions, target)

@register(day=7, level=2)
def level2(ip):
	positions = parse(ip)
	target = cheapest_level2(positions)
	return cost_level2(positions, target)

main(__name__)