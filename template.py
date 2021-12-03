#! /usr/bin/env python3

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split()



def part1(input_file):
    print("Part 1")
    x = read_file(input_file)



def part2(input_file):
    print("Part 2")
    x = read_file(input_file)


if __name__ == "__main__":
    part1("./test_input")
    print()
    part2("./test_input")
