#! /usr/bin/env python3
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")


def parse_coords(coords):
    tmp = []
    for coord in coords:
        c1, c2 = coord.split("->")
        tmp.append([c1.split(",") , c2.split(",")])
    return np.array(tmp, dtype=int)

def better_range(a, b):
    if b > a:
        return range(a,b+1)
    elif a > b:
        return range(a,b-1,-1)
    else:
        return [0,0]


def part1(input_file):
    print("Part 1")
    coords = parse_coords(read_file(input_file))
    line_map = np.zeros((1000, 1000))
    line_map_size_x, line_map_size_y = (0,0)

    for coord in coords:
        (x1, y1), (x2, y2)  = coord
        
        if abs(x1-x2) != 0 and abs(y1-y2) == 0:
            for dx in range(abs(x2-x1)+1): # +1 to include x2
                x = min(x1, x2)+dx
                y = y1
                line_map[y, x] += 1
                line_map_size_x = max(line_map_size_x, x)
                line_map_size_y = max(line_map_size_y, y)
        elif abs(x1-x2) == 0 and abs(y1-y2) != 0:
            for dy in range(abs(y2-y1)+1): # +1 to include y2
                x = x1
                y = min(y1, y2)+dy
                line_map[y, x] += 1
                line_map_size_x = max(line_map_size_x, x)
                line_map_size_y = max(line_map_size_y, y)
        else:
            # print(f"Ignored {coord=}")
            pass


    line_map = line_map[:line_map_size_y+1, :line_map_size_x+1]
    num_overlap = np.where(line_map >= 2)[0].size
    print(num_overlap)

    # print(coords)



def part2(input_file):
    print("Part 2")
    coords = parse_coords(read_file(input_file))
    line_map = np.zeros((5000, 5000), dtype=int)
    line_map_size_x, line_map_size_y = (0,0)

    for coord in coords:
        (x1, y1), (x2, y2)  = coord
        
        if abs(x1-x2) != 0 and abs(y1-y2) == 0:
            for dx in range(abs(x2-x1)+1): # +1 to include x2
                x = min(x1, x2)+dx
                y = y1
                line_map[y, x] += 1
                line_map_size_x = max(line_map_size_x, x)
                line_map_size_y = max(line_map_size_y, y)
        elif abs(x1-x2) == 0 and abs(y1-y2) != 0:
            for dy in range(abs(y2-y1)+1): # +1 to include y2
                x = x1
                y = min(y1, y2)+dy
                line_map[y, x] += 1
                line_map_size_x = max(line_map_size_x, x)
                line_map_size_y = max(line_map_size_y, y)
        else:
            for dx, dy in zip(better_range(0, x2-x1), better_range(0, y2-y1)):
                x = x1 + dx
                y = y1 + dy
                # print(coord, x,y)
                line_map[y, x] += 1
                line_map_size_x = max(line_map_size_x, x)
                line_map_size_y = max(line_map_size_y, y)


    line_map = line_map[:line_map_size_y+1, :line_map_size_x+1]
    # print(line_map)
    num_overlap = np.where(line_map >= 2)[0].size
    print(num_overlap)



if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
