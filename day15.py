import functools as ft
import heapq
import numpy as np
from shared import register, main
from utils import fiter

def parse(ip):
    rows = []

    for line in ip:
        line = line.strip()
        row = list(map(int, line))
        rows.append(row)

    return np.array(rows)

def index_in_bounds(position, shape):
    i, j = position
    height, width = shape
    return i >= 0 and j >= 0 and i < height and j < width

def adjacent_indices(position, shape):
    offsets = (
        np.array((0, -1)), # left
        np.array((0, 1)), # right
        np.array((-1, 0)), # up
        np.array((1, 0)), # down
    )

    return frozenset(
        filter(
            ft.partial(index_in_bounds, shape=shape),
            (tuple(position + offset) for offset in offsets),
        )
    )

def dijkstra(root, children, cost):
    queue = [(0, root)]
    heapq.heapify(queue)
    seen = set()

    while queue:
        cost_to_node, node = heapq.heappop(queue)
        yield node, cost_to_node

        for child in children(node):
            if child not in seen:
                seen.add(child)
                cost_to_child = cost_to_node + cost(child)
                heapq.heappush(queue, (cost_to_child, child))

@register(day=15, level=1)
def level1(ip):
    costs = parse(ip)
    start = (0, 0)
    shape = costs.shape
    end = (shape[0] - 1, shape[1] - 1)
    
    iterator = dijkstra(
        start,
        ft.partial(adjacent_indices, shape=shape),
        lambda i: costs[i]
    )

    path = []

    for i, cost in iterator:
        if i == end:
            return cost

        path.append(i)

def increment(costs):
    costs = (costs + 1) % 10
    costs += costs == 0
    return costs

def expand(costs):
    rows = []

    for i in range(5):
        row = []

        for j in range(5):
            row.append(fiter(increment, i + j, costs))

        rows.append(row)

    return np.block(rows)

@register(day=15, level=2)
def level2(ip):
    costs = expand(parse(ip))
    start = (0, 0)
    shape = costs.shape
    end = (shape[0] - 1, shape[1] - 1)
    
    iterator = dijkstra(
        start,
        ft.partial(adjacent_indices, shape=shape),
        lambda i: costs[i]
    )

    path = []

    for i, cost in iterator:
        if i == end:
            return cost

        path.append(i)

main(__name__)