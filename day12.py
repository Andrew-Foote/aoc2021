from collections import Counter, defaultdict
from shared import register, main, get_input

def parse(ip):
	for line in ip:
		yield line.strip().split('-')

	ip.close()

def restructure_data(edges):
	connections = defaultdict(lambda: set())

	for start, end in edges:
		if start != 'end' and end != 'start':
			connections[start].add(end)

		if start != 'start' and end != 'end':
			connections[end].add(start)

	return connections

def is_small(cave):
	return cave.lower() == cave

def cave_paths(connections, start, visited=None, max_visits=1):
	"""
	>>> connections = restructure_data(parse(get_input('12_example')))
	>>> for p in sorted(cave_paths(connections, 'start')):
	...     print(','.join(p))
	start,A,b,A,c,A,end
	start,A,b,A,end
	start,A,b,end
	start,A,c,A,b,A,end
	start,A,c,A,b,end
	start,A,c,A,end
	start,A,end
	start,b,A,c,A,end
	start,b,A,end
	start,b,end
	>>> s = set(cave_paths(connections, 'start', max_visits=2))
	>>> for l in
	start,A,b,A,b,A,c,A,end
	start,A,b,A,b,A,end
	start,A,b,A,b,end
	start,A,b,A,c,A,b,A,end
	start,A,b,A,c,A,b,end
	start,A,b,A,c,A,c,A,end
	start,A,b,A,c,A,end
	start,A,b,A,end
	start,A,b,d,b,A,c,A,end
	start,A,b,d,b,A,end
	start,A,b,d,b,end
	start,A,b,end
	start,A,c,A,b,A,b,A,end
	start,A,c,A,b,A,b,end
	start,A,c,A,b,A,c,A,end
	start,A,c,A,b,A,end
	start,A,c,A,b,d,b,A,end
	start,A,c,A,b,d,b,end
	start,A,c,A,b,end
	start,A,c,A,c,A,b,A,end
	start,A,c,A,c,A,b,end
	start,A,c,A,c,A,end
	start,A,c,A,end
	start,A,end
	start,b,A,b,A,c,A,end
	start,b,A,b,A,end
	start,b,A,b,end
	start,b,A,c,A,b,A,end
	start,b,A,c,A,b,end
	start,b,A,c,A,c,A,end
	start,b,A,c,A,end
	start,b,A,end
	start,b,d,b,A,c,A,end
	start,b,d,b,A,end
	start,b,d,b,end
	start,b,end
	"""

	if visited is None:
		visited = Counter()

	if is_small(start):
		visited = Counter(visited)
		visited[start] += 1

	if start == 'end':
		yield (start,)

	for node in connections[start]:
		if visited[node] < max_visits:
			for path_from_node in cave_paths(connections, node, visited, max_visits):
				yield (start, *path_from_node)

@register(day=12, level=1)
def level1(ip):
	connections = restructure_data(parse(ip))
	ps = cave_paths(connections, 'start')
	return sum(1 for path in ps)

@register(day=12, level=2)
def level2(ip):
	connections = restructure_data(parse(ip))
	ps = cave_paths(connections, 'start', max_visits=2)

	for p in ps:
		print(p)

	return sum(1 for path in ps)

main(__name__)