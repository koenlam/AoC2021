#! /usr/bin/env python3
import numpy as np
from numpy.core.numeric import full

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")



def parse_map(raw_map):
    return np.array([list(line) for line in raw_map], dtype=int)




def _valid_coord(y, x, max_y, max_x):
    if 0 <= y <= max_y and 0 <= x <= max_x:
        return True
    else:
        return False



def part1(input_file):
    print("Part 1")
    map = parse_map(read_file(input_file))
    cost_map = np.zeros(map.shape)
    visited_map = np.zeros(map.shape)-1

    start = (0,0) # (y,x)
    end = (map.shape[0]-1, map.shape[1]-1) # (y, x)
    
    map_y, map_x = map.shape


    # Visiting flags
    NOT, CURRENT, VISITED = (-1, 0, 1)

    valid_coord = lambda y, x: _valid_coord(y, x, map_y-1, map_x-1)

    dcoord = ((-1,0), (1,0), (0,-1), (0, 1))

    visited_map[start] = CURRENT

    map_changed = True
    while map_changed:
        map_changed = False
        for y in range(map_y):
            for x in range(map_x):
                if visited_map[y,x] == CURRENT:
                    for dy, dx in dcoord:
                        sy = y + dy
                        sx = x + dx
                        if valid_coord(sy, sx):
                            if visited_map[sy, sx] == NOT:
                                visited_map[sy, sx] = CURRENT
                                cost_map[sy, sx] = cost_map[y, x] + map[sy, sx]
                                map_changed = True
                            elif visited_map[sy, sx] == CURRENT or visited_map[sy, sx] == VISITED:
                                new_cost = cost_map[y, x] + map[sy, sx]
                                if new_cost < cost_map[sy, sx]:
                                    map_changed = True
                                    visited_map[sy, sx] = CURRENT
                                    cost_map[sy, sx] = new_cost
                            else:
                                raise ValueError(f"Invalid flag{visited_map[sy, sx]}")
                    visited_map[y,x] = VISITED
    print(f"lowest risk = {int(cost_map[end])}")



def create_full_map(map):
    # Very ugly  method to overcome the same shape limitation of np.concatenate:/
    row = map
    new_tile = map
    for _ in range(4):
        new_tile = (new_tile % 9) +1
        row = np.concatenate((row, new_tile), axis=1)
    full_map = row


    current_tile = (map % 9) + 1
    for _ in range(4):
        row = current_tile
        new_tile = current_tile
        
        for _ in range(4):
            new_tile = (new_tile % 9) +1
            row = np.concatenate((row, new_tile), axis=1)
        current_tile = (current_tile % 9) + 1
        full_map = np.concatenate((full_map, row), axis=0)
    return full_map
            




def part2(input_file):
    print("Part 2")
    map = parse_map(read_file(input_file))
    map = create_full_map(map)
     
    cost_map = np.zeros(map.shape)
    visited_map = np.zeros(map.shape)-1

    start = (0,0) # (y,x)
    end = (map.shape[0]-1, map.shape[1]-1) # (y, x)
    
    map_y, map_x = map.shape


    # Visiting flags
    NOT, CURRENT, VISITED = (-1, 0, 1)

    valid_coord = lambda y, x: _valid_coord(y, x, map_y-1, map_x-1)

    dcoord = ((-1,0), (1,0), (0,-1), (0, 1))

    visited_map[start] = CURRENT

    map_changed = True
    while map_changed:
        map_changed = False
        for y in range(map_y):
            for x in range(map_x):
                if visited_map[y,x] == CURRENT:
                    for dy, dx in dcoord:
                        sy = y + dy
                        sx = x + dx
                        if valid_coord(sy, sx):
                            if visited_map[sy, sx] == NOT:
                                visited_map[sy, sx] = CURRENT
                                cost_map[sy, sx] = cost_map[y, x] + map[sy, sx]
                                map_changed = True
                            elif visited_map[sy, sx] == CURRENT or visited_map[sy, sx] == VISITED:
                                new_cost = cost_map[y, x] + map[sy, sx]
                                if new_cost < cost_map[sy, sx]:
                                    map_changed = True
                                    visited_map[sy, sx] = CURRENT
                                    cost_map[sy, sx] = new_cost
                            else:
                                raise ValueError(f"Invalid flag{visited_map[sy, sx]}")
                    visited_map[y,x] = VISITED
    print(f"lowest risk = {int(cost_map[end])}")



if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
