import numpy as np
from shared import register, main

def parse(ip):
	return list(map(int, next(ip).split(',')))
	ip.close()

def restructure_data(ages):
	vec = np.zeros(9)

	for age in ages:
		vec[age] += 1

	return vec

TRANS = np.array([
	[0, 1, 0,  0, 0, 0,  0, 0, 0], # age0(t) = age1(t0)
	[0, 0, 1,  0, 0, 0,  0, 0, 0], # age1(t) = age2(t0)
	[0, 0, 0,  1, 0, 0,  0, 0, 0], # age2(t) = age3(t0)
	[0, 0, 0,  0, 1, 0,  0, 0, 0], # age3(t) = age4(t0)
	[0, 0, 0,  0, 0, 1,  0, 0, 0], # age4(t) = age5(t0)
	[0, 0, 0,  0, 0, 0,  1, 0, 0], # age5(t) = age6(t0)
	[1, 0, 0,  0, 0, 0,  0, 1, 0], # age6(t) = age7(t0) + age0(t0)
	[0, 0, 0,  0, 0, 0,  0, 0, 1], # age7(t) = age8(t0)
	[1, 0, 0,  0, 0, 0,  0, 0, 0], # age8(t) = age0(t0)
])

@register(day=6, level=1)
def level1(ip):
	ages = parse(ip)
	vec = restructure_data(ages)

	for _ in range(80):
		vec = TRANS @ vec

	return round(sum(vec))

main(__name__)