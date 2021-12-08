def common_value(first, *rest):
	assert all(i == first for i in rest)
	return first

def sgn(x):
	return x // abs(x)