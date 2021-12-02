#! /usr/bin/env python3

def read_file(filename):
    with open(filename) as f:
        return f.read().strip()



def part1(input_file):
    print("Part 1")
    instructions = [l.split() for l in read_file(input_file).split("\n")]
    hor_pos = 0
    depth = 0
    for dir, val in instructions:
        if dir == "forward":
            hor_pos += int(val)
        elif dir == "down":
            depth += int(val)
        elif dir == "up":
            depth -= int(val)
        else:
            raise ValueError(f"Unknown direction {dir}")
    print(f"{hor_pos=} | {depth=} | {hor_pos*depth=}")
    print()

def part2(input_file):
    print("Part 2")
    instructions = [l.split() for l in read_file(input_file).split("\n")]
    hor_pos = 0
    depth = 0
    aim = 0
    for dir, val in instructions:
        if dir == "forward":
            hor_pos += int(val)
            depth += int(val)*aim
        elif dir == "down":
            aim += int(val)
        elif dir == "up":
            aim -= int(val)
        else:
            raise ValueError(f"Unknown direction {dir}")
    print(f"{hor_pos=} | {depth=} | {hor_pos*depth=}")
    print()

if __name__ == "__main__":
    part1("./input")
    part2("./input")