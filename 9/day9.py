#! /usr/bin/env python3
from functools import reduce
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")




def parse_height_map(map):
    return np.array([list(m) for m in map], dtype=int)


def bound_coord(a, lb, ub):
    # print(a, lb, ub)
    return max(min(a, ub), lb)


def part1(input_file):
    print("Part 1")
    height_map = parse_height_map(read_file(input_file))
    
    height_map_y, height_map_x = height_map.shape

    bound_x = lambda x: bound_coord(x, 0, height_map_x-1)
    bound_y = lambda y: bound_coord(y, 0, height_map_y-1)

    low_points = []

    # Find low points
    for y in range(height_map_y):
        for x in range(height_map_x):
            dstep = (-1,0,1)
            
            # Check if it is a low point
            is_low_point = True
            for dy in dstep:
                for dx in dstep:
                    sy = bound_y(y + dy)
                    sx = bound_x(x + dx)

                    if sy == y and sx == x:
                        continue

                    if  height_map[y,x] >= height_map[sy, sx]:
                        is_low_point = False
                        break
                if is_low_point is False:
                    break
            if is_low_point is True:
                low_points.append((y,x))
    # print(low_points)

    sum_risk_levels = np.sum([height_map[low_point]+1 for low_point in low_points])
    print(f"{sum_risk_levels}")




def part2(input_file):
    print("Part 2")
    height_map = parse_height_map(read_file(input_file))
    
    height_map_y, height_map_x = height_map.shape

    bound_x = lambda x: bound_coord(x, 0, height_map_x-1)
    bound_y = lambda y: bound_coord(y, 0, height_map_y-1)

    low_points = []

    # Find low points
    for y in range(height_map_y):
        for x in range(height_map_x):
            dstep = (-1,0,1)
            
            # Check if it is a low point
            is_low_point = True
            for dy in dstep:
                for dx in dstep:
                    sy = bound_y(y + dy)
                    sx = bound_x(x + dx)

                    if sy == y and sx == x:
                        continue

                    if  height_map[y,x] >= height_map[sy, sx]:
                        is_low_point = False
                        break
                if is_low_point is False:
                    break
            if is_low_point is True:
                low_points.append((y,x))
    

    # Find basins
    basins_sizes = []
    for low_point in low_points:
        basin_map = np.zeros(height_map.shape)
        basin_map[low_point] = 1

        basin_height = 1
        basin_changed = True
        while basin_changed:
            basin_changed = False
            for y in range(height_map_y):
                for x in range(height_map_x):
                    if basin_map[y,x] == basin_height:
                        dstep = (-1,0,1)
                        
                        # Check if  neighbor is higher
                        # is_part_basin = True
                        for dy in dstep:
                            for dx in dstep:
                                sy = bound_y(y + dy)
                                sx = bound_x(x + dx)
                                if (sy == y and sx == x) or height_map[sy, sx] == 9 or (abs(sy-y)+abs(sx-x) != 1) or basin_map[sy, sx] >= basin_map[y,x]:
                                    continue

                                
                                if  height_map[sy, sx] > height_map[y, x]:
                                    # print("here", (sy, sx), height_map[sy, sx],  (y, x), height_map[y, x])
                                    # Add to basin
                                    basin_changed = True
                                    basin_map[sy,sx] = basin_height + 1
            basin_height += 1
        # print(basin_map)
        basins_sizes.append(np.where(basin_map > 0)[0].size)
    
    basins_multiply = reduce(lambda a, b: a*b, np.sort(basins_sizes)[-3:])
    print(f"{basins_multiply=}")


if __name__ == "__main__":
    # part1("./input")
    print()
    part2("./input")
