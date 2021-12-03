#! /usr/bin/env python3
import os


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split()



def part1(input_file):
    print("Part 1")
    nums = read_file(input_file)
    # print(nums)
    gamma_rate = ""
    epsilon_rate = ""

    for i in range(len(nums[0])):
        bit0_cnt = 0
        bit1_cnt = 0
        for num in nums:
            if num[i] == "0":
                bit0_cnt += 1
            elif num[i] == "1":
                bit1_cnt += 1
            else:
                raise ValueError(f"Unknown {num[i]=}" )

        assert bit0_cnt != bit1_cnt
        if bit0_cnt > bit1_cnt:
            gamma_rate += "0"
            epsilon_rate += "1"
        elif  bit0_cnt < bit1_cnt:
            gamma_rate += "1"
            epsilon_rate += "0"
    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)

    print(f"{gamma_rate=}, {epsilon_rate=}, {gamma_rate*epsilon_rate=}")



def part2(input_file):
    def _get_most_common_value(nums, index):
        bit0_cnt = 0
        bit1_cnt = 0
        for num in nums:
            if num[i] == "0":
                bit0_cnt += 1
            elif num[i] == "1":
                bit1_cnt += 1
            else:
                raise ValueError(f"Unknown {num[i]=}" )

        if bit0_cnt ==  bit1_cnt:
            return "0.5"
        elif bit0_cnt > bit1_cnt:
            return "0"
        else:
            return "1"


    print("Part 2")
    nums = read_file(input_file)


    # Oxygen generator rating
    nums_cpy = nums.copy()
    for i in range(len(nums[0])):
        mst_val = _get_most_common_value(nums_cpy, i)

        if mst_val in ("1", "0.5"):
            nums_cpy = list(filter(lambda num: num[i] == "1", nums_cpy))
        else:
            nums_cpy = list(filter(lambda num: num[i] == "0", nums_cpy))
        if len(nums_cpy) == 1:
            break
    
    assert len(nums_cpy) == 1
    oxygen_rating = int(nums_cpy[0], 2)


    # CO2 scrubber rating
    nums_cpy = nums.copy()
    for i in range(len(nums[0])):
        mst_val = _get_most_common_value(nums_cpy, i)

        if mst_val in ("1", "0.5"):
            nums_cpy = list(filter(lambda num: num[i] == "0", nums_cpy))
        else:
            nums_cpy = list(filter(lambda num: num[i] == "1", nums_cpy))
        if len(nums_cpy) == 1:
            break
    
    assert len(nums_cpy) == 1
    CO2_rating = int(nums_cpy[0], 2)

    print(f"{oxygen_rating=}, {CO2_rating=}, {oxygen_rating*CO2_rating=}")

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
