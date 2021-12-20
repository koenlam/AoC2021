#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n\n")


def parse_input(raw_input):
    img_alg, input_img = raw_input

    img_alg = list(img_alg.replace("\n", "").replace(".", "0").replace("#", "1"))
    img_alg = [int(b) for b in img_alg]

    input_img = np.array([list(b) for b in input_img.replace(".", "0").replace("#", "1").split("\n")], dtype=int)

    return img_alg, input_img

def add_border(img, border_padding, border_width=2):
    if border_padding == 0:
        gen_border = np.zeros
    elif border_padding == 1:
        gen_border = np.ones
    else:
        raise ValueError(f"{border_padding} is invalid")


    img_y, img_x = img.shape
    
    side_border_x = gen_border((img_y, border_width), dtype=int)
    side_border_y = gen_border((border_width, img_x+border_width*2), dtype=int) # +6 to compensate for border x

    # horizontal border
    img = np.concatenate((side_border_x, img, side_border_x), axis=1)
    # Vertical border
    img = np.concatenate((side_border_y, img, side_border_y), axis=0)

    return img


def get_bin_number(img, y, x):
    # Get a square 3 x 3 pixels and turn it into a binary number
    img_y, img_x = img.shape

    assert y-1 >= 0 
    assert y+1 < img_y
    assert x-1 >= 0
    assert x+1 < img_x


    bin_str = ""
    for yy in range(y-1, y+2):
        for xx in range(x-1, x+2):
            bin_str += str(img[yy, xx])

    return int(bin_str, 2)


def enchance_img(input_img, img_alg):
    img_y, img_x = input_img.shape
    output_img = np.empty((img_y-2, img_x-2), dtype=int)
    for y in range(1, img_y-1): # Not including a border of 1 pixel  as that one consits of the infinite pixels
        for x in range(1, img_x-1):
            enchance_idx = get_bin_number(input_img, y, x)
            output_pixel = img_alg[enchance_idx]
            output_img[y-1,x-1] = output_pixel
    return output_img

def save_img(img):
    img_y, img_x = img.shape

    with open("img.txt", "w") as f:
        for y in range(img_y):
            for x in range(img_x):
                bit = '#' if img[y,x] == 1 else '.'
                f.write(bit)
            f.write("\n")

def part1(input_file):
    print("Part 1")
    img_alg, input_img = parse_input(read_file(input_file))

    # Enchance image
    border_padding = 0
    for _ in range(2):
        input_img = add_border(input_img, border_padding=border_padding)
        input_img = enchance_img(input_img, img_alg)
        border_padding = img_alg[int(str(border_padding)*9,2)]


    num_lit_pixels = np.where(input_img > 0)[0].size
    print(f"{num_lit_pixels=}")
    

def part2(input_file):
    print("Part 2")
    img_alg, input_img = parse_input(read_file(input_file))

    # Enchance image
    border_padding = 0
    for _ in range(50):
        input_img = add_border(input_img, border_padding=border_padding)
        input_img = enchance_img(input_img, img_alg)
        border_padding = img_alg[int(str(border_padding)*9,2)]


    num_lit_pixels = np.where(input_img > 0)[0].size
    print(f"{num_lit_pixels=}")
    


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
