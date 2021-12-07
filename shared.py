from collections import defaultdict
import itertools as it

def get_input(day):
	return open(f'input/day{day}.txt')

solutions = defaultdict(lambda: {})

def register(day, level):
	def wrap(solution):
		def wrapper():
			return solution(get_input(day))

		solutions[day][level] = wrapper
		return wrapper

	return wrap

def main(name):
	if name == '__main__':
		import doctest
		doctest.testmod()

		import sys

		day = int(sys.argv[1])
		level = int(sys.argv[2])
		print(solutions[day][level]())