import numpy as np
from shared import register, main

def parse(ip):
	return np.array([
		list(map(int, line.strip()))
		for line in ip
	])

	ip.close()

@register(day=9, level=1)
def level1(ip):
	hmap = parse(ip)
	width, height = hmap.shape
	
	right = np.block([
		[hmap[:, 1:], np.full(height, 10).reshape(-1, 1)]
	])

	down = np.block([
		[hmap[1:, :]],
		[np.full(width, 10)],
	])

	left = np.block([
		[np.full(height, 10).reshape(-1, 1), hmap[:, :-1]]
	])

	up = np.block([
		[np.full(width, 10)],
		[hmap[:-1, :]],
	])

	low = (hmap < right) & (hmap < down) & (hmap < left) & (hmap < up)
	return sum(hmap[low] + 1)

main(__name__)