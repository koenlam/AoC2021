#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce


def read_file(filename):
    with open(filename) as f:
        return f.read().strip()


def parse_input(raw_input):
    x_low, x_high = re.findall(r"x=-*\d+..-*\d+", raw_input)[0].strip("x=").split("..")
    y_low, y_high = re.findall(r"y=-*\d+..-*\d+", raw_input)[0].strip("y=").split("..")
    return int(x_low), int(x_high), int(y_low), int(y_high)



def in_target(x, y, x_low, x_high, y_low, y_high):
    # Returns:
    #  1 for within target
    #  0 Before target
    #  -1 missed target
    if x_low <= x <= x_high and y_low <= y <= y_high:
        return 1
    elif x > x_high or y < y_low:
        return -1
    else:
        return 0



def puzzle(input_file):
    print("Part 1")
    target_x_low, target_x_high, target_y_low, target_y_high = parse_input(read_file(input_file))
    # print(target_x_low, target_x_high, target_y_low, target_y_high)

    in_target_short = lambda x, y : in_target(x, y, target_x_low, target_x_high, target_y_low, target_y_high)
    (T_BEFORE, T_WITHIN, T_MISSED) = (0, 1, -1)


    
    y_maxs = []
    for vx_start in range(1,target_x_high+1):
        for vy_start in range(target_y_low, 1000):
            vy = vy_start
            vx = vx_start
            x_sim = 0
            y_sim = 0
            y_max = 0 

            while in_target_short(x_sim, y_sim) == T_BEFORE:
                x_sim += vx
                y_sim += vy
                vy -= 1
                vx = max(0, vx-1)
                y_max = max(y_sim, y_max)

            if in_target_short(x_sim, y_sim) == T_WITHIN:
                y_maxs.append(y_max)
            


    print(max(y_maxs))
    print("Part 2")
    print(len(y_maxs))



if __name__ == "__main__":
    puzzle("./input")
