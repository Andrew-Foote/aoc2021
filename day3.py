from collections import Counter
from shared import register, main

@register(day=3, level=1)
def level1(ip):
	sums = Counter()

	for line in ip:
		for i, c in enumerate(line.strip()):
			sums[i] += int(c)

	ip.close()

	gamma_rate = []
	epsilon_rate = []

	for i, _ in enumerate(sums):
		bits = ['0', '1']

		# 1 most common
		# (case where sums[i] == 500 is ambiguous)
		if sums[i] > 500:
			bits.reverse()

		most_common, least_common = bits
		gamma_rate.append(most_common)
		epsilon_rate.append(least_common)

	gamma_rate = ''.join(gamma_rate)
	epsilon_rate = ''.join(epsilon_rate)
	return int(gamma_rate, 2) * int(epsilon_rate, 2)

main(__name__)