from shared import register, main
from utils import parse_digits

def parse(ip):
	for line in ip:
		patterns, value = [part.strip() for part in line.split('|')]
		patterns = sorted(map(frozenset, patterns.split()), key=len)
		value = list(map(frozenset, value.split()))
		yield patterns, value

	ip.close()

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
		for _, value in parse(ip)
	)

#    nsegs  2 3 4 5 5 5 6 6 6 7
# in order: 1 7 4 2~3~5 0~6~9 8

DIGIT_PATTERNS = tuple(map(frozenset, (
	'abcefg', # 0
	'cf', # 1
	'acdeg', # 2
	'acdfg', # 3
	'bcdf', # 4
	'abdfg', # 5
	'abdefg', # 6
	'acf', # 7
	'abcdefg', # 8
	'abcdfg' # 9
)))

PATTERN_DIGITS = {pattern: digit for digit, pattern in enumerate(DIGIT_PATTERNS)}

def decode(data):
	for patterns, value in data:
		codes = {}

		def add_code(original, encoded):
			codes[frozenset(original)] = encoded

		def encode(pattern):
			return codes[frozenset(pattern)]

		codes[DIGIT_PATTERNS[1]] = patterns[0]
		codes[DIGIT_PATTERNS[7]] = patterns[1]
		codes[DIGIT_PATTERNS[4]] = patterns[2]
		codes[DIGIT_PATTERNS[8]] = patterns[9]

		# We know which three patterns correspond to 2, 3 or 5 (the ones of
		# size 5), though we don't know which of the three is which digit.
		size_5_patterns = patterns[3:6]

		# We know which three patterns correspond to 0, 6 or 9 (the ones of
		# size 6), though we don't know which of the three is which digit.
		size_6_patterns = patterns[6:9]

		# pat(1) = cf, pat(7) = acf, hence pat(7) - pat(1) = a
		add_code('a', encode('acf') - encode('cf'))

		# pat(7) can't give us any more information---we already know a, so
		# pat(7) just tells us cf, which we already know from pat(1)

		# pat(4) = bcdf, hence pat(4) - pat(1) = bd
		add_code('bd', encode('bcdf') - encode('cf'))

		# pat(8) = abcdefg, hence pat(8) - a = bcdefg
		add_code('bcdefg', encode('abcdefg') - encode('a'))
		# hence (pat(8) - a) - pat(4) = eg
		add_code('eg', encode('bcdefg') - encode('bcdf'))

		# that's all we can do with the easy digits.
		# how about...
		# 2 = acdeg, 3 = acdfg, 5 = abcdfg, hence
		# pat(2) ^ pat(3) ^ pat(5) = adg, so we can work out dg
		add_code('adg', frozenset.intersection(*size_5_patterns))
		add_code('dg', encode('adg') - encode('a'))
		# we know bd, we know dg, hence...
		add_code('b', encode('bd') - encode('dg'))
		# and then we can deduce d and g
		add_code('d', encode('bd') - encode('b'))
		add_code('g', encode('dg') - encode('d'))
		# and once we have g, we can deduce e, since we know eg
		add_code('e', encode('eg') - encode('g'))

		# now neither pat(4) nor pat(8) has any new info... both reduce to cf
		# so, what can we do with the size 6 patterns?
		# 0 = abcefg, 6 = abdefg, 9 = abcdfg
		# their intersection is abfg
		add_code('abfg', frozenset.intersection(*size_6_patterns))
		add_code('f', encode('abfg') - (encode('a') | encode('b') | encode('g')))
		add_code('c', encode('cf') - encode('f'))

		segment_decode = {
			next(iter(encode(segment))): segment
			for segment in 'abcdefg'
		}

		def decode_part(part):
			return frozenset(segment_decode[segment] for segment in part)

		# alright, now we just have to decode the values by inverting the segment perms
		decoded_parts = [decode_part(part) for part in value]
		digits = [PATTERN_DIGITS[part] for part in decoded_parts] 
		yield parse_digits(digits, 10)

@register(day=8, level=2)
def level2(ip):
	return sum(decode(parse(ip)))

main(__name__)