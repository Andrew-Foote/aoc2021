import numpy as np
from shared import register, main, get_input

def parse(ip):
    """
    >>> calls, boards = parse(get_input('4_example'))
    >>> calls
    [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    >>> len(boards)
    3
    >>> boards[0].tolist()
    [[22, 13, 17, 11, 0], [8, 2, 23, 4, 24], [21, 9, 14, 16, 7], [6, 10, 3, 18, 5], [1, 12, 20, 15, 19]]
    >>> boards[1].tolist()
    [[3, 15, 0, 2, 22], [9, 18, 13, 17, 5], [19, 8, 7, 25, 23], [20, 11, 10, 24, 4], [14, 21, 16, 12, 6]]
    >>> boards[2].tolist()
    [[14, 21, 17, 24, 4], [10, 16, 15, 9, 19], [18, 8, 23, 26, 20], [22, 11, 13, 6, 5], [2, 0, 12, 3, 7]]
    """
    calls = list(map(int, next(ip).strip().split(',')))
    boards = []
    board = []

    for line in ip:
        line = line.strip()

        if line:
            row = list(map(int, line.split()))
            board.append(row)

            if len(board) >= 5:
                boards.append(np.array(board))
                board = []

    ip.close()
    return calls, boards

def bingo(calls, boards):
    marks = [np.zeros((5, 5), dtype=bool) for _ in boards]

    for call in calls:
        for i, board in enumerate(boards):
            marks[i] |= board == call
        
        yield call, [board_marks.copy() for board_marks in marks]

def wins(marks):
    return marks.all(0).any() or marks.all(1).any()

def score(call, winner, marks):
    return winner[~marks].sum() * call

@register(day=4, level=1)
def level1(ip):
    calls, boards = parse(ip)

    for call, marks in bingo(calls, boards):
        for board, board_marks in zip(boards, marks):
            if wins(board_marks):
                return score(call, board, board_marks)

@register(day=4, level=2)
def level2(ip):
    calls, boards = parse(ip)
    won = set()

    for call, marks in bingo(calls, boards):
        for i, board in enumerate(boards):
            board_marks = marks[i]

            if wins(board_marks):
                won.add(i)

            if len(won) >= len(boards):
                return score(call, board, board_marks)

main(__name__)