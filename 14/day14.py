#! /usr/bin/env python3
import numpy as np
from collections import defaultdict

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n\n")


def parse_input(x):
    return x[0], dict([xx.split(" -> ") for xx in x[1].split("\n")])


def iter_pair(x):
    tmp  = []
    for i in range(0, len(x)):
        pair = x[i:i+2]
        if len(pair) >= 2:
            tmp.append(pair)
    return tmp


def count_elements(x):
    element_count = dict()
    for el in set(x):
        element_count[el] = x.count(el)
    return element_count

def part1(input_file):
    print("Part 1")
    template, rules = parse_input(read_file(input_file))
    # print(template)
    # print(rules)

    # Simulate pair insertion
    for _ in range(10):
        tmp = template[0]
        for pair in iter_pair(template):
            # print(pair)
            tmp += rules[pair] + pair[1] 
        template = tmp
        # print(template)

    # Find most common pair
    element_count = count_elements(template)

    element_most_common_count = max(element_count.values())
    element_least_common_count = min(element_count.values())

    count_difference = element_most_common_count - element_least_common_count
    print(f"{count_difference=}")




def parse_template(template):
    pair_dict = defaultdict(lambda : 0)
    for pair in iter_pair(template):
        pair_dict[pair] += 1
    return pair_dict


def construct_template_string(template_dict):
    unordered_template = ""
    for pair in template_dict:
        unordered_template += pair * template_dict[pair]
    return unordered_template





def part2(input_file):
    print("Part 2")
    template, rules = parse_input(read_file(input_file))
    template = parse_template(template)
    # print(template)
    # print(rules)

    # Simulate pair insertion
    for i in range(40):
        # print(i)
        new_template = template.copy()
        for pair in template:
            pair_count = template[pair]
            el_insert = rules[pair]

            new_template[pair[0] + el_insert] += pair_count
            new_template[el_insert + pair[1]] += pair_count
            new_template[pair] -= pair_count
        template = new_template

    #Find most common pair
    # Note every element is counted double
    element_count = defaultdict(lambda: 0)
    for pair in template:
        element_count[pair[0]] += template[pair]
        element_count[pair[1]] += template[pair]
    
    element_most_common_count = max(element_count.values())
    element_least_common_count = min(element_count.values())

    # Divide by 2 because every element is counted double due to the overlapping pairs
    # Also round up because the first and last element of the polymer is not counted double and thus can result in an uneven number
    count_difference = int(np.ceil(element_most_common_count/2 - element_least_common_count/2))
    print(f"{count_difference=}")


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
