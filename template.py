#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")


def part1(input_file):
    print("Part 1")
    x = read_file(input_file)
    print(x)


def part2(input_file):
    print("Part 2")
    x = read_file(input_file)


if __name__ == "__main__":
    part1("./test_input")
    print()
    # part2("./test_input")
