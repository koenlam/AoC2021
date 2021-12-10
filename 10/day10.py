#! /usr/bin/env python3
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")



def part1(input_file):
    print("Part 1")
    lines = read_file(input_file)
    # print(lines)

    r_chucks = ["(", "[", "{", "<"]
    l_chucks = [")", "]", "}", ">"]
    r2l_chucks = dict(zip(r_chucks, l_chucks))

    illegal_points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    error_score = 0
    stack = []
    for line in lines:
        for c in line:
            if c in r_chucks:
                stack.append(c)
            elif c in l_chucks:
                r_c = stack.pop()
                if r2l_chucks[r_c] == c:
                    # Correct
                    pass
                else:
                    # Incorrect
                    # print(line, f"Expected {r2l_chucks[r_c]}, but found {c} instead")
                    error_score += illegal_points[c]
                    break


    print(f"{error_score=}")



def part2(input_file):
    print("Part 2")
    lines = read_file(input_file)
    # print(lines)

    r_chucks = ["(", "[", "{", "<"]
    l_chucks = [")", "]", "}", ">"]
    r2l_chucks = dict(zip(r_chucks, l_chucks))

    # Find illegal lines
    illegal_lines = []
    stack = []
    for i, line in enumerate(lines):
        for c in line:
            if c in r_chucks:
                stack.append(c)
            elif c in l_chucks:
                r_c = stack.pop()
                if r2l_chucks[r_c] == c:
                    # Correct
                    pass
                else:
                    # Incorrect
                    illegal_lines.append(i)
                    break


    scores = []
    score_table = {")": 1, "]": 2, "}": 3, ">": 4}
    # Find incomplete lines
    for i, line in enumerate(lines):
        if i not in illegal_lines:
            stack = []
            for c in line:
                if c in r_chucks:
                    stack.append(c)
                elif c in l_chucks:
                    r_c = stack.pop()
                    if r2l_chucks[r_c] == c:
                        # Correct
                        pass
                    else:
                        raise ValueError("How did you get here?")
            # If line is incomplete
            if len(stack):
                score = 0
                for r_c in stack[::-1]:
                    score *= 5
                    score += score_table[r2l_chucks[r_c]]
                scores.append(score)
    # print(scores)
    middle_score = sorted(scores)[len(scores)//2]
    print(f"{middle_score=}")
                

            


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
