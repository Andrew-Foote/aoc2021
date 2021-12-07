import re
import numpy as np
from shared import register, main

DIR_UNIT_VECS = {k: np.array(v) for k, v in {
	'forward': [0, 1],
	'down': [1, 0],
	'up': [-1, 0],
}.items()}

@register(day=2, level=1)
def level1(ip):
	pos = np.array([0, 0])

	for line in ip:
		dir_, mag = re.match(r'(\w+) (\d+)', line).groups()
		vel = int(mag) * DIR_UNIT_VECS[dir_]
		pos += vel

	return pos[0] * pos[1]

main(__name__)