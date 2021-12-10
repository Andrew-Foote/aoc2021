import numpy as np
from shared import register, main
from utils import product

def parse(ip):
	return np.array([
		list(map(int, line.strip()))
		for line in ip
	])

	ip.close()

def shifts(matrix):
	height, width = matrix.shape

	# right
	yield np.block([
		[matrix[:, 1:], np.full(height, 10).reshape(-1, 1)]
	])

	# down
	yield np.block([
		[matrix[1:, :]],
		[np.full(width, 10)],
	])

	# left
	yield np.block([
		[np.full(height, 10).reshape(-1, 1), matrix[:, :-1]]
	])

	# up
	yield np.block([
		[np.full(width, 10)],
		[matrix[:-1, :]],
	])

@register(day=9, level=1)
def level1(ip):
	hmap = parse(ip)
	right, down, left, up = shifts(hmap)
	low = (hmap < right) & (hmap < down) & (hmap < left) & (hmap < up)
	return sum(hmap[low] + 1)

@register(day=9, level=2)
def level2(ip):
	hmap = parse(ip)
	height, width = hmap.shape
	#right, down, left, up = shifts(hmap)
	basin = -(1 + (hmap == 9)) # -2 where there's a 9, -1 otherwise

	basin_count = 0

	# all we need to do is find the contiguous areas of 1s
	for i in range(height):
		for j in range(height):
			if hmap[i, j] == 9:


			# -2 = it's a peak
			# -1 = still haven't decided what basin it's in
			if basin[i, j] == -1:
				# look at the top and left, if either have a basin set, that's our basin
				if i > 0 and basin[i - 1, j] > -1:
					basin[i, j] = basin[i - 1, j]
				elif j > 0 and basin[i, j - 1] > -1:
					basin[i, j] = basin[i, j - 1]
				else:
					# otherwise, it's a new basin
					basin[i, j] = basin_count
					basin_count += 1

	print(basin[:10, :10])

	basin_sizes = []

	for basin_id in range(basin_count):
		basin_sizes.append(sum(hmap[basin == basin_id]))

	basin_sizes.sort()
	return product(basin_sizes[-3:])


main(__name__)