
def read_file(filename):
    with open(filename) as f:
        return f.read().strip()


def part1():
    print("Part 1")
    measurements = [int(m) for m in read_file("./input").split("\n")]
    num_increases = sum([a < b for a, b in zip(measurements, measurements[1:])])
    print(f"{num_increases=}")
    print()

def part2():
    print("Part 2")
    measurements = [int(m) for m in read_file("./input").split("\n")]
    measurement_sliding = [a + b + c for a, b, c in zip(measurements, measurements[1:], measurements[2:])]
    num_increases = sum([a < b for a, b in zip(measurement_sliding, measurement_sliding[1:])])
    print(f"{num_increases=}")
    print()


if __name__ == "__main__":
    part1()
    part2()