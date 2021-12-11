#! /usr/bin/env python3
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")


def bound_coord(a, lb, ub):
    # print(a, lb, ub)
    return max(min(a, ub), lb)

def parse_flashing_lights(x):
    return set(zip(x[0], x[1]))


def part1(input_file):
    print("Part 1")
    lights = np.array([list(l) for l in read_file(input_file)], dtype=int)

    lights_y, lights_x = lights.shape
    bound_x = lambda x: bound_coord(x, 0, lights_x-1)
    bound_y = lambda y: bound_coord(y, 0, lights_y-1)
    
    num_flashes = 0
    for i in range(100):
        # print(i)
        # print(lights)
        lights += 1
        flashing_lights = parse_flashing_lights(np.where(lights > 9))
        has_flashed = set()
        while len(flashing_lights) > 0:
            # Update energy levels of surrounding octopuses 
            for y, x in flashing_lights:
                has_flashed.add((y,x))
                num_flashes += 1
                dd = (-1,0,1)

                has_visited = set()
                for dy in dd:
                    for dx in dd:
                        sy = bound_y(y + dy)
                        sx = bound_x(x + dx)

                        if (sy == y and sx == x) or (sy, sx) in has_visited:
                            continue

                        has_visited.add((sy,sx))
                        lights[sy, sx] += 1
                break

            flashing_lights = parse_flashing_lights(np.where(lights > 9)) - has_flashed
        if len(has_flashed):
            for y, x in has_flashed:
                lights[y,x] = 0
    print(f"{num_flashes=}")



def part2(input_file):
    print("Part 2")
    lights = np.array([list(l) for l in read_file(input_file)], dtype=int)

    lights_y, lights_x = lights.shape
    bound_x = lambda x: bound_coord(x, 0, lights_x-1)
    bound_y = lambda y: bound_coord(y, 0, lights_y-1)
    
    num_flashes = 0
    i = 0
    while True:
        i += 1
        # print(i)
        # print(lights)
        lights += 1
        flashing_lights = parse_flashing_lights(np.where(lights > 9))
        has_flashed = set()
        while len(flashing_lights) > 0:
            # Update energy levels of surrounding octopuses 
            for y, x in flashing_lights:
                has_flashed.add((y,x))
                num_flashes += 1
                dd = (-1,0,1)

                has_visited = set()
                for dy in dd:
                    for dx in dd:
                        sy = bound_y(y + dy)
                        sx = bound_x(x + dx)

                        if (sy == y and sx == x) or (sy, sx) in has_visited:
                            continue

                        has_visited.add((sy,sx))
                        lights[sy, sx] += 1
                break

            flashing_lights = parse_flashing_lights(np.where(lights > 9)) - has_flashed
        if len(has_flashed) == lights.size:
            print("All flash step =",i)
            break
        elif len(has_flashed):
            for y, x in has_flashed:
                lights[y,x] = 0


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
