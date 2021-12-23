#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce
from copy import deepcopy


def read_file(filename):
    with open(filename) as f:
        return f.read().strip()


def parse_map(raw_map, side_room_size=2):
    amphipods = re.findall(r"\w", raw_map)


    num_side_rooms = len(amphipods) // side_room_size
    map = []
    for i, _ in enumerate(amphipods[:num_side_rooms]):
        # side_room = [amphipods[i], amphipods[i+num_side_rooms]]

        side_room = [amphipods[i+j*num_side_rooms] for j in range(side_room_size)]

        map.append(side_room)

    hallway = [None, None] + [None]*num_side_rooms +  [None] * (num_side_rooms-1)  + [None, None]

    goal = [[amphipod] * side_room_size  for amphipod in ["A", "B", "C", "D"]]


    cost = {"A": 1, "B": 10, "C": 100, "D":1000}

    hallway_translate = dict(zip(range(num_side_rooms), range(2, num_side_rooms*2+1, 2)))


    return map, hallway, goal, cost, hallway_translate


def is_goal_reached(map, goal):
    for sideroom_map, side_room_goal in zip(map, goal):
        for amphipod_map, amphipod_goal in zip(sideroom_map, side_room_goal):
            if amphipod_map != amphipod_goal:
                return False
    return True


def gen_possible_hallway_pos(sideroom_idx, hallway, hallway_translate):
    possible_moves = []
    
    # Go back
    pos = hallway_translate[sideroom_idx]
    while pos > 0:
        pos -= 1
        if pos not in hallway_translate.values():
            # Skip rooms above siderooms
            # print(pos, hallway)
            if hallway[pos] is None:
                possible_moves.append((pos, abs(pos-hallway_translate[sideroom_idx])))
            else:
                # Path blocked by another amphipod
                break
    
    # Go forwards
    pos = hallway_translate[sideroom_idx]
    while pos < len(hallway)-1:
        pos += 1
        if pos not in hallway_translate.values():
            # Skip rooms above siderooms
            if hallway[pos] is None:
                possible_moves.append((pos, abs(pos-hallway_translate[sideroom_idx])))
            else:
                # Path blocked by another amphipod
                break
    return possible_moves


def gen_possible_sideroom_pos(hallway_idx, map, hallway, hallway_translate, map_goal):
    possible_moves = []
    hallway_tranlate_r = dict(zip(hallway_translate.values(), hallway_translate.keys()))

    #Go back
    pos = hallway_idx
    while pos > 0:
        pos -= 1
        if hallway[pos] is not None:
            # Blocked path
            break

        if pos in hallway_translate.values():
            # possible sideroom to go in
            for side_idx, sideroom_spot in list(enumerate(map[hallway_tranlate_r[pos]]))[::-1]:
                if sideroom_spot == hallway[hallway_idx]:
                    continue
                elif sideroom_spot is not None:
                    break
                elif hallway[hallway_idx] == map_goal[hallway_tranlate_r[pos]][side_idx]:
                    assert map[hallway_tranlate_r[pos]][side_idx] is None
                    # print(map[hallway_tranlate_r[pos]])
                    possible_moves.append((hallway_tranlate_r[pos], side_idx, abs(hallway_idx-pos)+side_idx))
                    break

    
    #Go forwards
    pos = hallway_idx
    while pos < len(hallway)-1:
        pos += 1
        if hallway[pos] is not None:
            # Blocked path
            break

        if pos in hallway_translate.values():
            # possible sideroom to go in
            for side_idx, sideroom_spot in list(enumerate(map[hallway_tranlate_r[pos]]))[::-1]:
                if sideroom_spot == hallway[hallway_idx]:
                    continue
                elif sideroom_spot is not None:
                    break
                elif hallway[hallway_idx] == map_goal[hallway_tranlate_r[pos]][side_idx]:
                    assert map[hallway_tranlate_r[pos]][side_idx] is None
                    # print(map[hallway_tranlate_r[pos]])
                    possible_moves.append((hallway_tranlate_r[pos], side_idx, abs(hallway_idx-pos)+side_idx))
                    break

    return possible_moves

flatten = lambda x: tuple([xxx for xx in x for xxx in xx])
min_cost = 1000000
path_costs = defaultdict(lambda: 1000000)


def walk(map, hallway, map_goal, move_cost, hallway_translate, map_cost=0, depth=0):
    global min_cost, path_costs
    # print("---- DEPTH", depth)
    if map_cost >= path_costs[(flatten(map), tuple(hallway))]:
        return
    else:
        path_costs[(flatten(map), tuple(hallway))] = map_cost
    
    if is_goal_reached(map, map_goal):
        if map_cost < min_cost:
            min_cost = map_cost
    else:
        # Move the amphipod to the hallway
        for j, side_room in enumerate(map):
            for i, amphipod in enumerate(side_room):
                if amphipod is None:
                    # Skip empty spots
                    continue
                
                if i != 0: 
                    # Check amphipod can move out of side room
                    side_room_open = True
                    for ii in range(i):
                        if side_room[ii] is not None:
                            side_room_open = False
                            break
                    if side_room_open is False:
                        break
                
                # print("JAKLSDJSKAL", amphipod, map_goal[j])
                if amphipod == map_goal[j][i]:
                    # Possible that amphipod is at correct position
                    if i == len(side_room)-1:
                        # Amphipod at the last position
                        break
                    
                    amphipod_at_goal = True
                    for amphipod_below in side_room[i+1:]:
                        if amphipod_below != amphipod:
                            amphipod_at_goal = False
                            break
                    if amphipod_at_goal:
                        break

                # Go through all possible hallway positions
                possible_hall_ways = gen_possible_hallway_pos(j, hallway, hallway_translate)
                for pos, steps in possible_hall_ways:

                    cost = move_cost[amphipod]*(steps+i+1)
                    map_n = deepcopy(map)
                    map_n[j][i] = None
                    hallway_n = hallway.copy()
                    hallway_n[pos] = amphipod
                    walk(map_n, hallway_n, map_goal, move_cost, hallway_translate, map_cost=map_cost+cost, depth=depth+1)
        
        # Move hallway amphipod into sideroom
        for h_idx, amphipod in enumerate(hallway):
            if amphipod is not None:
                possible_sideroom_pos = gen_possible_sideroom_pos(h_idx, map, hallway, hallway_translate, map_goal)
                for sideroom_idx, sideroom_pos, steps in possible_sideroom_pos:
                    cost = move_cost[amphipod]*(steps+1)
                    map_n = deepcopy(map)
                    map_n[sideroom_idx][sideroom_pos] = amphipod
                    hallway_n = hallway.copy()
                    hallway_n[h_idx] = None

                    walk(map_n, hallway_n, map_goal, move_cost, hallway_translate, map_cost=map_cost+cost, depth=depth+1)

def part1(input_file):
    global min_cost, path_costs
    min_cost = 1000000
    path_costs = defaultdict(lambda: 1000000)

    print("Part 1")
    map, hallway, map_goal, move_cost, hallway_translate = parse_map(read_file(input_file))    
    walk(map, hallway, map_goal, move_cost, hallway_translate)
    print(f"{min_cost=}")





def part2(input_file):
    global min_cost, path_costs
    min_cost = 1000000
    path_costs = defaultdict(lambda: 1000000)

    print("Part 2")
    map, hallway, map_goal, move_cost, hallway_translate = parse_map(read_file(input_file), side_room_size=4)
    walk(map, hallway, map_goal, move_cost, hallway_translate)
    print(f"{min_cost=}")

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input_p2")
