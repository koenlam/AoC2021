#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce



def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")

def parse_input(raw_input):
    player1, player2_ = raw_input

    get_starting_pos = lambda x : int(re.findall("\d+", x)[-1])

    return get_starting_pos(player1), get_starting_pos(player2_)

class DeterministicDice:
    def __init__(self, num_sides=100):
        self.num_rolls = 0
        self.num_sides = num_sides
    
    def roll(self):
        self.num_rolls += 1
        return ((self.num_rolls-1) % self.num_sides) + 1


def part1(input_file):
    print("Part 1")
    p1_pos, p2_pos = parse_input(read_file(input_file))
    p1_points, p2_points = (0, 0)

    dice = DeterministicDice()

    while p1_points < 1000 or p2_points < 100:
        p1_pos = ((p1_pos + dice.roll() + dice.roll() + dice.roll()-1) % 10) + 1
        p1_points +=  p1_pos

        if p1_points >= 1000:
            break

        p2_pos =  ((p2_pos + dice.roll() + dice.roll() + dice.roll()-1) % 10) + 1
        p2_points +=  p2_pos


    losing_points = min(p1_points, p2_points)
    print(losing_points * dice.num_rolls)




def part2(input_file):
    print("Part 2")
    p1_pos, p2_pos = parse_input(read_file(input_file))
    p1_points, p2_points = (0, 0)

    class DicePlayer():
        def __init__(self, pos, points, dice_dict):
            self.paths = defaultdict(lambda : defaultdict(list))
            self.paths_possible = defaultdict(lambda : defaultdict(int))
            self.pos = pos
            self.points = points
            self.dice_dict = dice_dict
            self.find_all_possible_outcomes(self.pos, self.points)
            self.calc_possible_paths()

        def find_all_possible_outcomes(self, p_pos, p_points, p_rolls=[], target_score=21):
            self.paths[len(p_rolls)][p_points].append(p_rolls)        
            if p_points >= target_score:
                return
            else:
                for p_roll in range(3,10):
                    p_pos_n = ((p_pos + p_roll - 1) % 10) + 1
                    p_points_n = p_points + p_pos_n
                    self.find_all_possible_outcomes(p_pos_n, p_points_n, p_rolls +[p_roll])


        def calc_possible_paths(self):
            for iteration in self.paths:
                for p_point in self.paths[iteration]:
                    num_possibilities = 0
                    for path in self.paths[iteration][p_point]:
                        num_possibilities_path = 1
                        for roll in path:
                            num_possibilities_path *= self.dice_dict[roll]
                        num_possibilities += num_possibilities_path
                    self.paths_possible[iteration][p_point] = num_possibilities



    dice_dict = dict()
    dice_dict[3] = 1 # 111
    dice_dict[4] = 3 # 112
    dice_dict[5] = 3 + 3 # 113 122
    dice_dict[6] = 6 + 1 #123 222 
    dice_dict[7] = 3 + 3 # 133 223
    dice_dict[8] = 3 # 233
    dice_dict[9] = 1 # 333


    p1 = DicePlayer(p1_pos, p1_points, dice_dict)
    p2 = DicePlayer(p2_pos, p2_points, dice_dict)

    p1_wins_all = 0
    p2_wins_all = 0

    max_iter = max(p1.paths_possible.keys())
    assert max_iter ==  max(p2.paths_possible.keys())

    p2_prev_lost = 0
    for iter in range(max_iter+1):
        # Check p1 wins
        p1_lost = 0
        p1_wins = 0
        for p1_points in p1.paths_possible[iter]:
            if p1_points < 21:
                p1_lost += p1.paths_possible[iter][p1_points]
            else:
                p1_wins += p1.paths_possible[iter][p1_points]
        

        # Check p2 wins
        p2_lost = 0
        p2_wins = 0
        for p2_points in p2.paths_possible[iter]:
            if p2_points < 21:
                p2_lost += p2.paths_possible[iter][p2_points]
            else:
                p2_wins += p2.paths_possible[iter][p2_points]

        p1_wins_all += p1_wins * p2_prev_lost
        p2_wins_all += p2_wins * p1_lost

        p2_prev_lost = p2_lost
    
    
    # print(f"{p1_wins_all=}")
    # print(f"{p2_wins_all=}")

    print(max(p1_wins_all, p2_wins_all))



if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
