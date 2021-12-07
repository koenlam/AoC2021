#! /usr/bin/env python3
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split(",")



def part1(input_file):
    print("Part 1")
    crabs = np.array(read_file(input_file), dtype=int)
    median = np.median(crabs)
    cheapest_fuel_needed = np.sum(np.abs(crabs-median))
    # print(crabs, np.median(crabs))
    print(f"{cheapest_fuel_needed=}")






def part2(input_file):
    print("Part 2")
    crabs = np.array(read_file(input_file), dtype=int)

    fuel_list = []
    medians = []
    for m in range(np.max(crabs)):
        fuel = 0
        for crab in crabs:
            fuel += np.sum(np.arange(1, np.abs(crab - m)+1))
        fuel_list.append(fuel)
        medians.append(m)
    cheapest_fuel_needed = np.min(fuel_list)
    print(f"{cheapest_fuel_needed=}")

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
