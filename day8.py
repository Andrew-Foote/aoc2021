from shared import register, main

def parse(ip):
	for line in ip:
		patterns, value = [part.strip() for part in line.split('|')]
		patterns = list(map(frozenset, patterns.split()))
		value = list(map(frozenset, value.split()))
		yield patterns, value

	ip.close()

# 0 uses 6 segments
# 1 uses 2 segments
# 2 uses 5 segments
# 3 uses 5 segments
# 4 uses 4 segments
# 5 uses 5 segments
# 6 uses 6 segments
# 7 uses 3 segments
# 8 uses 7 segments
# 9 uses 6 segments

# map from number of segments to digit
SIZE_TO_DIGIT = {
	2: 1,
	3: 7,
	4: 4,
	7: 8,
}

@register(day=8, level=1)
def level1(ip):
	return sum(
		sum(len(part) in SIZE_TO_DIGIT for part in value)
		for pattern, value in parse(ip)
	)

main(__name__)