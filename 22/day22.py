#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce




def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")

def parse_steps(raw_steps):
    steps = []
    for line in raw_steps:
        operation, cube = line.split()
        cube = np.array([np.array(re.findall(r"-?\d+", axis), dtype=int) for axis in cube.split(",")],dtype=int)
        steps.append((operation, cube))

    return steps


def part1(input_file):
    print("Part 1")
    steps = parse_steps(read_file(input_file))
    
    reactor = np.zeros((200, 200, 200), dtype=int)
    offset = 100

    for instruction, cube in steps:
        if np.where(cube > 50)[0].size or np.where(cube < -50)[0].size:
            # print("Skipped", cube)
            # print(np.where(cube > 50), np.where(cube < -50))
            continue
        x, y, z = cube + offset


        if instruction == 'on':
            reactor[z[0]:z[1]+1, y[0]:y[1]+1, x[0]:x[1]+1] = 1
        elif instruction == 'off':
            reactor[z[0]:z[1]+1, y[0]:y[1]+1, x[0]:x[1]+1] = 0
        else:
            raise ValueError(f"{instruction} is invalid")
   
    print(np.where(reactor > 0)[0].size)



LOW, HIGH = (0,1)
LOW_IN, HIGH_IN, WHOLLY_IN, WHOLLY_OUT = (1,2,3,4)
def check_cube_overlap(cube1, cube2):
    # Checks if cube2 overlaps with cube1 and returns the overlapping region if it overlaps otherwise None

    overlap_flags = []
    # Check if which part of cube2 overlaps with cube1
    for i, (coord1, coord2) in enumerate(zip(cube1, cube2)):
        overlap = 0
        
        if coord1[LOW] <= coord2[LOW] <= coord1[HIGH]:
            overlap |= LOW_IN
        if coord1[LOW] <= coord2[HIGH] <= coord1[HIGH]:
            overlap |= HIGH_IN
        
        if coord2[LOW] < coord1[LOW]  and coord2[HIGH] > coord1[HIGH]:
            assert overlap == 0
            overlap = WHOLLY_OUT

        if coord2[HIGH] < coord1[LOW] or coord2[LOW] > coord1[HIGH]:
            assert overlap == 0
            return None # No overlap
        overlap_flags.append(overlap)
    # print(overlap_flags)

    # Calculate the overlapping cube
    cube_overlap = []
    for over_lap_flag, coord1, coord2 in zip(overlap_flags, cube1, cube2):
        if over_lap_flag == LOW_IN:
            coord_overlap = coord2
            coord_overlap[HIGH] = coord1[HIGH]
        elif over_lap_flag == HIGH_IN:
            coord_overlap = coord2
            coord_overlap[LOW] = coord1[LOW]
        elif over_lap_flag == WHOLLY_IN:
            coord_overlap = coord2
        elif over_lap_flag == WHOLLY_OUT:
            coord_overlap = coord1
        else:
            raise ValueError(f"{over_lap_flag=} is invalid")

        cube_overlap.append(coord_overlap)

    return np.array(cube_overlap,dtype=int)



def part2(input_file):
    print("Part 2")
    # Unfortunately I couldn't solve this one on my own and had to look up the solution on "https://pastebin.com/XXLcH5M0"
    # I was close with the solution however I couldn't figure out how to solve the part of multiple overlaps
    # The solution I looked up use a toggle to solve it which was genius
    steps = parse_steps(read_file(input_file))

    x_idx, y_idx, z_idx = (0,1,2)
    cubes = []
    opposite_instr = {"on": "off", "off":"on"}

    for new_instr, new_cube in steps:
        new_cubes = []
        for prev_instr, prev_cubes in cubes:
            overlap_cube = check_cube_overlap(prev_cubes.copy(), new_cube.copy())
            if overlap_cube is not None:
                overlap_instr = opposite_instr[prev_instr]
                new_cubes.append((overlap_instr, overlap_cube))
        if new_instr == "on":
            cubes.append((new_instr, new_cube))
        cubes += new_cubes


    volume = 0
    for instr, cube in cubes:
        new_volume = (abs(cube[x_idx][HIGH] - cube[x_idx][LOW]) + 1) * (abs(cube[y_idx][HIGH] - cube[y_idx][LOW]) + 1) * (abs(cube[z_idx][HIGH] - cube[z_idx][LOW]) + 1)  
        # print(new_volume, instr, cube)
        if instr == "on":
            volume += new_volume
        else:
            volume -= new_volume
    print(volume)




if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
