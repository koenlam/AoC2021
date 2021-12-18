#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce

from copy import deepcopy


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")


def generate_sum(numbers, sum=[]):
    if len(numbers) == 0:
        return sum
    else:
        if sum != []:
            return generate_sum(numbers[1:], sum=[sum, eval(numbers[0])])
        else:
            return generate_sum(numbers[1:], sum=numbers[0])

def parse_snailfish_number(numbers):
    return [eval(n) for n in numbers]


snailfish_depth_paths = []


def snailfish_depth_walk(number, path=[]):
    if isinstance(number, int):
        snailfish_depth_paths.append(path)
    else:
        for i, n in enumerate(number):
            snailfish_depth_walk(n, path + [i])


def snailfish_number_get(number, path):
    n = number.copy()
    p = path.copy()
    while p:
        idx = p.pop(0)
        # print("HERE", idx, path, n)
        n = n[idx]
    return n

def snailfish_number_set(number, path, new_number=None, add_number=None):
    n = number
    for idx in path[:-1]:
        n = n[idx]
    if new_number is not None:
        n[path[-1]] = new_number 
    elif add_number is not None:
        n[path[-1]] += add_number
    else:
        raise TypeError("Both new_number and add_number not set")



def snailfish_reduce(number):
    global snailfish_depth_paths
    snailfish_depth_paths = []

    snailfish_depth_walk(number)
    # print(snailfish_depth_paths)
    # Check for exploding pairs
    for i, path in enumerate(snailfish_depth_paths):
        if len(path) == 5: # 5 because the regular number is also counted as a depth level
            # Explode the pair
            first_regular_number_left = snailfish_number_get(number, snailfish_depth_paths[i-1]) if i-1 >= 0 else None
            first_regular_number_right = snailfish_number_get(number, snailfish_depth_paths[i+2]) if i+2 < len(snailfish_depth_paths) else None

            exploding_number_left = snailfish_number_get(number, path)
            exploding_number_right =snailfish_number_get(number, snailfish_depth_paths[i+1])

            # print("test", first_regular_number_left)
            # print("test2",first_regular_number_right)
            
            # Add first regular number to the left of the exploding pair
            if first_regular_number_left is not None:
                snailfish_number_set(number, snailfish_depth_paths[i-1], add_number=exploding_number_left)
            if first_regular_number_right is not None:
                snailfish_number_set(number, snailfish_depth_paths[i+2], add_number=exploding_number_right)
            # print("FINAL")
            # print(number)

            # Set exploding pair to zero
            snailfish_number_set(number, path[:-1], new_number=0)
            # print("HERERRRR", number)
            return snailfish_reduce(number)
        elif len(path) > 5:
            raise ValueError(f"{path} too long")
    
    # Check for splits
    for i, path in enumerate(snailfish_depth_paths):
        n = snailfish_number_get(number, path)
        if n >= 10:
            # Split the number
            pair = [int(np.floor(n/2)), int(np.ceil(n/2))]
            # print(pair)
            snailfish_number_set(number, path, new_number=pair)
            # print("SPLIT", number)
            return snailfish_reduce(number)
    # Nothing left to reduce
    return number
                





def add_snailfish_number(n1, n2):
    # Check if numbers has to be reduced
    n1 = snailfish_reduce(n1)
    n2 = snailfish_reduce(n2)
    return snailfish_reduce([n1, n2])

def add_snailfish_numbers(numbers):
    numbers = deepcopy(numbers)
    n = numbers[0]
    for n2 in numbers[1:]:
        n = add_snailfish_number(n, n2)
    return n


def find_magnitude(number):
    if isinstance(number, int):
        return number
    else:
        n1 = find_magnitude(number[0])
        n2 = find_magnitude(number[1])
        # print(n1, n2)
        return 3*n1+2*n2



def part1(input_file):
    print("Part 1")
    numbers = parse_snailfish_number(read_file(input_file))
    n = add_snailfish_numbers(numbers)
    magnitude = find_magnitude(n)
    print(f"{magnitude=}")

def part2(input_file):
    print("Part 2")
    numbers = parse_snailfish_number(read_file(input_file))

    magnitudes = []
    for i, n1 in enumerate(numbers):
        for j, n2 in enumerate(numbers):
            if i != j:
                n = add_snailfish_numbers([n1, n2])
                magnitude = find_magnitude(n)
                magnitudes.append(magnitude)
    # print(sorted(magnitudes))
    largest_magnitude = max(magnitudes)
    print(f"{largest_magnitude=}")


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
