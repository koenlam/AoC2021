#! /usr/bin/env python3
import numpy as np
import re

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n\n")



def parse_instructions(x):
    dots = np.array([xx.split(',')[::-1] for xx in  x[0].split('\n')], dtype=int)
    folds = x[1].split('\n')
    return dots, folds

def parse_fold(fold):
    if re.findall("y=", fold):
        return int(re.search("\d+", fold).group(0)), None
    elif re.findall("x=", fold):
        return None, int(re.search("\d+", fold).group(0))
    else:
        raise ValueError(f"Invalid {fold=}")


def part1(input_file):
    print("Part 1")
    dots, folds = parse_instructions(read_file(input_file))

    paper_max_y = max(dots, key=lambda x: x[0])[0]+1
    paper_max_x = max(dots, key=lambda x: x[1])[1]+1

    paper = np.zeros((paper_max_y, paper_max_x), dtype=int)
    for dot_y, dot_x in dots:
        paper[dot_y, dot_x] = 1
    

    for fold in folds:
        fold_y, fold_x = parse_fold(fold)

        if fold_y is not None:
            paper1 = paper[:fold_y, ]
            paper2 = paper[fold_y+1:, ]

            assert paper1.shape == paper2.shape
            
            paper = paper1 + paper2[::-1,]
        elif fold_x is not None:
            paper1 = paper[:,:fold_x]
            paper2 = paper[:,fold_x+1:]

            assert paper1.shape == paper2.shape
            
            paper = paper1 + paper2[:,::-1]
        break
        

    num_dots = np.where(paper > 0)[0].size

    print(f"{num_dots=}")


def print_paper(paper):
    for line in paper:
        for c in line:
            if c == 0:
                print(".",end=' ')
            else:
                print("#",end=' ')
        print()



def part2(input_file):
    print("Part 2")
    dots, folds = parse_instructions(read_file(input_file))

    paper_max_y = max(dots, key=lambda x: x[0])[0]+1
    paper_max_x = max(dots, key=lambda x: x[1])[1]+1

    paper = np.zeros((paper_max_y, paper_max_x), dtype=int)
    for dot_y, dot_x in dots:
        paper[dot_y, dot_x] = 1
    

    for fold in folds:
        fold_y, fold_x = parse_fold(fold)

        if fold_y is not None:
            paper1 = paper[:fold_y, ]
            paper2 = paper[fold_y+1:, ]

            assert paper1.shape == paper2.shape
            
            paper = paper1 + paper2[::-1,]
        elif fold_x is not None:
            paper1 = paper[:,:fold_x]
            paper2 = paper[:,fold_x+1:]

            assert paper1.shape == paper2.shape
            
            paper = paper1 + paper2[:,::-1]
    print_paper(paper)

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
