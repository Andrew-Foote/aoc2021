import itertools as it
import numpy as np
from shared import register, main

def parse(ip):
	return np.array([
		list(map(int, line.strip()))
		for line in ip
	])

	ip.close()

def flash(state, i, j):
	height, width = state.shape

	if i > 0:
		state[i - 1, j] += 1

		if j > 0:
			state[i - 1, j - 1] += 1
	
		if j < width - 1:
			state[i - 1, j + 1] += 1

	if i < height - 1:
		state[i + 1, j] += 1
	
		if j > 0:
			state[i + 1, j - 1] += 1

		if j < width - 1:
			state[i + 1, j + 1] += 1

	if j > 0:
		state[i, j - 1] += 1

	if j < width - 1:
		state[i, j + 1] += 1

def step(state):
	"""
	>>> state = np.array([[1, 1, 1, 1, 1], [1, 9, 9, 9, 1], [1, 9, 1, 9, 1], [1, 9, 9, 9, 1], [1, 1, 1, 1, 1]])
	>>> step(state)
	9
	>>> state
	array([[3, 4, 5, 4, 3],
	       [4, 0, 0, 0, 4],
	       [5, 0, 0, 0, 5],
	       [4, 0, 0, 0, 4],
	       [3, 4, 5, 4, 3]])
	"""
	width, height = state.shape
	state += 1
	flashed = set()
	doing_flashes = True

	while doing_flashes:
		for i, j in it.product(range(height), range(width)):
			if (i, j) not in flashed and state[i, j] > 9:
				flash(state, i, j)
				flashed.add((i, j))
				break
		else:
			doing_flashes = False

	for i, j in flashed:
		state[i, j] = 0

	return len(flashed)

@register(day=11, level=1)
def level1(ip):
	state = parse(ip)
	flashed_count = 0

	for _ in range(100):
		flashed_count += step(state)

	return flashed_count

@register(day=11, level=2)
def level2(ip):
	state = parse(ip)

	for i in it.count():
		flashed_count = step(state)

		if flashed_count == 100:
			return i + 1 # off-by-one error? not sure why


main(__name__)