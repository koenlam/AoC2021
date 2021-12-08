#! /usr/bin/env python3
from collections import defaultdict
import numpy as np
import re

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")



def part1(input_file):
    print("Part 1")
    output_values= " ".join([lines.split(" | ")[-1] for lines in read_file(input_file)])

    num_seg_1 = 2
    num_seg_4 = 4
    num_seg_7 = 3
    num_seg_8 = 7

    num_digits = 0
    for seg in output_values.split():
        for cmp_seg_len in (num_seg_1, num_seg_4, num_seg_7, num_seg_8):
            if len(seg) == cmp_seg_len:
                num_digits += 1

    print(f"{num_digits=}")


def string_sort(x):
    return "".join(sorted(x))


def string_remove(string1, string2):
    s = ""
    for s1 in string1:
        if s1 not in string2:
            s += s1
    return s



def string_include(string1, string2):
    for s in string2:
        if s not in string1:
            return False
    return True


def part2(input_file):
    print("Part 2")
    segment_values = [lines.split(" | ") for lines in read_file(input_file)]

    # 0: 6 -
    # 1: 2 u
    # 2: 5 +
    # 3: 5 +
    # 4: 3 u
    # 5: 5 +
    # 6: 6 -
    # 7: 3 u
    # 8: 7 u
    # 9: 6 -


    num_seg_1 = 2
    num_seg_4 = 4
    num_seg_7 = 3
    num_seg_8 = 7

    num_seg = {1:num_seg_1, 4:num_seg_4, 7:num_seg_7, 8:num_seg_8}


    seg_translator = dict()


    sum = 0
    for train, test in segment_values:
        train = [string_sort(x) for x in train.split()]
        test = [string_sort(x) for x in test.split()]

        ######## TRAINING ########
        decoded_digits = dict()
        for d in train:
            for num, seg_len in num_seg.items():
                if len(d) == seg_len:
                    decoded_digits[num] = d

        for s in decoded_digits.values():
            train.remove(s)
        
        # a = 7 - 1
        seg_translator['a'] = string_remove(decoded_digits[7], decoded_digits[1])

        # g = everywhere except at 1, 4, 7    
        for seg in "abcdefg":
            if seg not in decoded_digits[1]+decoded_digits[4]+decoded_digits[7]:
                is_g = True
                for d in train:
                    if seg not in d:
                        is_g = False
                        break
                if is_g:
                    seg_translator['g'] = seg
        
        
        # 9 = 4 + a
        decoded_digits[9] = string_sort(decoded_digits[4] + seg_translator['a'] + seg_translator['g'])
        train.remove(decoded_digits[9])

        # e = 8 - 9
        seg_translator['e'] = string_remove(decoded_digits[8], decoded_digits[9])

        # 0 = len(6) + all of 1
        for d in train:
            if len(d) == 6 and d != decoded_digits[9] and string_include(d, decoded_digits[1]):
                decoded_digits[0] = d
        train.remove(decoded_digits[0])

        # 6 = len(6) + not 0 or 9
        for d in train:
            if len(d) == 6:
                decoded_digits[6] = d
        train.remove(decoded_digits[6])

        # d = 8 - 0
        seg_translator['d'] = string_remove(decoded_digits[8], decoded_digits[0])

        # 5 = 6 - e
        decoded_digits[5] = string_remove(decoded_digits[6], seg_translator['e'])
        train.remove(decoded_digits[5])

        # 3 = has 1 in it
        for d in train:
            if string_include(d, decoded_digits[1]):
                decoded_digits[3] = d
        train.remove(decoded_digits[3])


        # 2 is left
        decoded_digits[2] = train.pop()
            
        ######## TESTING ########
        decoded_digits_rev = {v:k for k, v in decoded_digits.items()}
        val = ""
        for d in test:
            val += str(decoded_digits_rev[d])
        sum += int(val)

    print(f"{sum=}")

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
