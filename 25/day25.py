#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce


def read_file(filename):
    with open(filename) as f:
        return f.read().strip()

def parse_input(raw_input):
    map = raw_input.replace(">", "1").replace("v", "2").replace(".", "0")
    map = np.array([list(line) for line in map.split("\n")], dtype=int)
    return map


def puzzle(input_file):
    print("Day 25")
    map = parse_input(read_file(input_file))
    map_y, map_x = map.shape
    # print(map.shape)
    # return

    overflow_x = lambda x: x % (map_x)
    overflow_y = lambda y: y % (map_y)

    is_changed = True 
    step = 0
    while is_changed:
        # print(map)
        is_changed = False
        moving_cucumbers = []
        # Check which cucumbers to move
        # Check east moving
        for y in range(map_y):
            for x in range(map_x):
                if map[y,x] == 1:
                    if map[y, overflow_x(x+1)] == 0:
                        moving_cucumbers.append((y, x, y, overflow_x(x+1), 1))
                        is_changed = True

        # Move cucumbers 
        for old_y, old_x, new_y, new_x, sea_type in moving_cucumbers:
            map[old_y, old_x] = 0
            map[new_y, new_x] = sea_type

        moving_cucumbers = []
        # Check moving south
        for y in range(map_y):
            for x in range(map_x):
                if map[y,x] == 2:
                    if map[overflow_y(y+1), x] == 0:
                        moving_cucumbers.append((y, x, overflow_y(y+1), x, 2))
                        is_changed = True

        # Move cucumbers 
        for old_y, old_x, new_y, new_x, sea_type in moving_cucumbers:
            map[old_y, old_x] = 0
            map[new_y, new_x] = sea_type


        step += 1
    
    print(step)
        






if __name__ == "__main__":
    puzzle("./input")