import re
import numpy as np
from shared import register, main

DIR_UNIT_VECS = {k: np.array(v) for k, v in {
	'forward': [0, 1],
	'down': [1, 0],
	'up': [-1, 0],
}.items()}

# dimensions are [aim, depth, horizontal position]

def dir_unit_vec_lv2(dir_, pos):
	return np.array({
		'forward': [0, pos[0], 1],
		'down': [1, 0, 0],
		'up': [-1, 0, 0]
	}[dir_])

def parse(ip):
	for line in ip:
		dir_, mag = re.match(r'(\w+) (\d+)', line).groups()
		yield dir_, int(mag)

	ip.close()

@register(day=2, level=1)
def level1(ip):
	pos = np.array([0, 0])

	for dir_, mag in parse(ip):
		vel = mag * DIR_UNIT_VECS[dir_]
		pos += vel

	return pos[0] * pos[1]

@register(day=2, level=2)
def level2(ip):
	pos = np.array([0, 0, 0])

	for dir_, mag in parse(ip):
		vel = mag * dir_unit_vec_lv2(dir_, pos)
		pos += vel

	return pos[1] * pos[2]

main(__name__)