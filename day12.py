from collections import defaultdict
from shared import register, main

def parse(ip):
	for line in ip:
		yield line.strip().split('-')

	ip.close()

def restructure_data(edges):
	connections = defaultdict(lambda: set())

	for start, end in edges:
		connections[start].add(end)
		connections[end].add(start)

	del connections['end']
	return connections

def is_small(cave):
	return cave.lower() == cave

def cave_paths(connections, start, visited):
	if is_small(start):
		visited = visited | {start}

	if start == 'end':
		yield (start,)

	for node in connections[start]:
		if node not in visited:
			for path_from_node in cave_paths(connections, node, visited):
				yield (start, *path_from_node)

@register(day=12, level=1)
def level1(ip):
	connections = restructure_data(parse(ip))
	ps = cave_paths(connections, 'start', frozenset())
	return sum(1 for path in ps)

main(__name__)