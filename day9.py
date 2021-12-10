from collections import Counter
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
	basin_map = {}
	next_basin_id = 0

	for i in range(height):
		for j in range(width):
			if hmap[i, j] < 9:
				basin = basin_map.get((i - 1, j), None)
				left_basin = basin_map.get((i, j - 1), None)

				if basin is None:
					if left_basin is None:
						basin = next_basin_id
						next_basin_id += 1
					else:
						basin = left_basin
				elif left_basin is not None and left_basin != basin:
					# merge the basins
					for idx, basin_at_idx in basin_map.items():
						if basin_at_idx == left_basin:
							basin_map[idx] = basin

				basin_map[i, j] = basin

	basin_sizes = Counter()

	for i, basin in basin_map.items():
		basin_sizes[basin] += 1

	largest_three = [size for basin, size in basin_sizes.most_common()][:3]
	return product(largest_three)

main(__name__)