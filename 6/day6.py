#! /usr/bin/env python3
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split(",")



def part1(input_file):
    print("Part 1")
    fish = np.array(read_file(input_file), dtype=int)

    num_days = 80
    for _ in range(num_days):
        num_new_fish = np.where(fish == 0)[0].size
        fish -= 1
        fish = np.where(fish < 0, 6, fish)
        fish = np.concatenate((fish, np.ones(num_new_fish)*8))
        # print(fish)
    num_fish = fish.size
    print(f"{num_fish=}")




def parse_fish(fish):
    # Convert list of internal timers -> internal timer x num fish 
    tmp = [0 for _ in range(9)]
    for f in fish:
        tmp[f] += 1
    return tmp

def part2(input_file):
    print("Part 2")
    fish = parse_fish(map(int, read_file(input_file)))
    # print(fish)
    num_days = 256
    for _ in range(num_days):
        num_new_fish = fish.pop(0)
        fish.append(0)
        fish[6] += num_new_fish
        fish[8] += num_new_fish
        # print(fish)
    num_fish = sum(fish)
    print(f"{num_fish=}")




if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
