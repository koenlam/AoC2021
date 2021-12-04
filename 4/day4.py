#! /usr/bin/env python3
import numpy as np


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n\n")

def check_bingo(board_tickoff):
    assert board_tickoff.shape[0] == board_tickoff.shape[1]
    x = board_tickoff.shape[0]
    for i in range(x):
        if np.sum(board_tickoff[i,:]) == x or np.sum(board_tickoff[:,i]) == x:
            return True
    return False



def part1(input_file):
    print("Part 1")
    raw_input = read_file(input_file)
    bingo_seq, boards = (raw_input[0], raw_input[1:])
    bingo_seq = np.array(bingo_seq.split(","), dtype=int)
    boards = np.array([[row.split() for row in board.split("\n")] for board in boards], dtype=int)
    boards_tickoff = [np.zeros(board.shape, dtype=int) for board in boards ]
    # print(bingo_seq)
    is_bingo = False
    bingo_result = None
    for num in bingo_seq:
        for board, board_tickoff in zip(boards, boards_tickoff):
            board_tickoff += (1.0*np.isin(board, num)).astype(int)
            if check_bingo(board_tickoff) is True:
                is_bingo = True
                bingo_result = num*np.sum(board[np.logical_not(board_tickoff)])
                break
        if is_bingo:
            break
    print(f"{bingo_result=}")


def part2(input_file):
    print("Part 2")
    raw_input = read_file(input_file)
    bingo_seq, boards = (raw_input[0], raw_input[1:])
    bingo_seq = np.array(bingo_seq.split(","), dtype=int)
    boards = np.array([[row.split() for row in board.split("\n")] for board in boards], dtype=int)
    boards_tickoff = [np.zeros(board.shape, dtype=int) for board in boards]

    bingo_results = []
    bingo_boards = []
    for i, num in enumerate(bingo_seq):
        for ii, (board, board_tickoff) in enumerate(zip(boards, boards_tickoff)):
            board_tickoff += (1.0*np.isin(board, num)).astype(int)
            if check_bingo(board_tickoff) is True and ii not in bingo_boards:
                bingo_result = num*np.sum(board[np.logical_not(board_tickoff)])
                bingo_results.append((i, bingo_result))
                bingo_boards.append(ii)
    last_win = max(bingo_results, key=lambda x: x[0])
    print(f"{last_win=}")


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
