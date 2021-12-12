#! /usr/bin/env python3
from os import path
import numpy as np
from collections import defaultdict

def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")



def parse_edges(raw_edges):
    edges = defaultdict(list)
    for edge in raw_edges:
        n1, n2 = edge.split("-")
        edges[n1].append(n2)
        edges[n2].append(n1)
    return edges


def is_small_cave(node):
    return node.islower()



paths = []
def walk(node, edges, current_path=[]):
    current_path.append(node)
    # print("HERE", node, current_path)
    if node == 'end':
        paths.append(current_path)
        return
    elif len(edges[node]) == 0:
        # print("DEAD", current_path)
        return
    else:
        for next_node in edges[node]:
            if is_small_cave(next_node) and next_node in current_path:
                # print("DEAD2", node, next_node, current_path)
                pass
            else:
                walk(next_node, edges, current_path.copy())



def part1(input_file):
    global paths
    print("Part 1")
    edges = parse_edges(read_file(input_file))
    paths = []

    walk('start', edges)
    num_paths = len(paths)
    print(f"{num_paths=}")
    



def walk2(node, edges, current_path=[], has_small_cave_visited=False):
    current_path.append(node)
    # print("HERE", node, current_path)
    if node == 'end':
        paths.append(current_path)
        return
    elif len(edges[node]) == 0:
        # print("DEAD", current_path)
        return
    else:
        for next_node in edges[node]:
            has_small_cave_visited_local = has_small_cave_visited
            if is_small_cave(next_node):
                if next_node in current_path:
                    if has_small_cave_visited is True or next_node in ['start', 'end']:
                        # print("DEAD2", node, next_node, current_path)
                        continue
                    else:
                        # print("SETTING", node, next_node, current_path)
                        has_small_cave_visited_local = True
            
            walk2(next_node, edges, current_path.copy(), has_small_cave_visited_local)




def part2(input_file):
    global paths
    print("Part 2")
    edges = parse_edges(read_file(input_file))
    paths = []

    walk2('start', edges)
    num_paths = len(paths)
    print(f"{num_paths=}")

if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
