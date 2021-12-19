#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce

from copy import deepcopy

def read_file(filename):
    with open(filename) as f:
        return f.read().strip()


def parse_input(raw_input):
    return [[np.array(coord.split(","), dtype=int) for coord in scanner.split("\n")[1:]] for scanner in raw_input.split("\n\n")]
    
    # for scanner in raw_input.split("\n\n"):
    #     for coord in scanner.split("\n")[1:]:
    #         print(coord)


def get_distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)

def overlapping_coord(dists1, dists2):
    for dist in dists1:
        if dist in dists2:
            return True
    return False

def num_overlapping_dists(dists1, dists2):
    num_dists = 0
    for dist1 in dists1:
        if dist1 in dists2:
            num_dists += 1
    return num_dists

def puzzle(input_file):
    print("Part 1")
    scanners = parse_input(read_file(input_file))


    # Calculate all distances between coords
    scanners_coord_dist = []
    for ii, scanner in enumerate(scanners):
        scanners_coord_dist.append([])
        for i, coord1 in enumerate(scanner):
            scanners_coord_dist[ii].append([])
            for j, coord2 in enumerate(scanner):
                if i != j:
                    dist = get_distance(coord1, coord2)
                    scanners_coord_dist[ii][i].append(dist)
                    # print(coord1, coord2, dist)

    # print(scanners_coord_dist)


    # Find the pair of scanners that have at least 12 of the same beacons
    visited_pairs = []
    overlapping_pairs = []

    for i1, scanner_dists1 in enumerate(scanners_coord_dist):
        for i2, scanner_dists2 in enumerate(scanners_coord_dist):
            if i1 != i2 and (i1,i2) not in visited_pairs:
                visited_pairs.append((i1, i1))
                visited_pairs.append((i2, i1))
                # Compare the results of each scanner
                num_overlap = 0
                for c1, coord1_dists in enumerate(scanner_dists1):
                    for c2, coord2_dists in enumerate(scanner_dists2):
                        if overlapping_coord(coord1_dists, coord2_dists):
                            num_overlap += 1
                            break
                # print(i1, i2, num_overlap)
                if num_overlap >= 12:
                    overlapping_pairs.append((i1, i2))
    # print(overlapping_pairs)
    
    # Find the relative position of the scanners compared to scanner 0
    known_scanners = {0: np.array([0,0,0], dtype=int)}
    beacon_locations = set(tuple([tuple(beacon) for beacon in scanners[0]]))
    while overlapping_pairs:
        is_found = False
        # Find a pair where one of the scanners has a known location
        for i, overlap_pair in enumerate(overlapping_pairs):
            for known_scanner in known_scanners.keys():
                if known_scanner in overlap_pair:
                    pair = overlapping_pairs.pop(i)
                    known_scanner_pair_idx = pair.index(known_scanner)
                    known_scanner_id = pair[known_scanner_pair_idx]
                    unknown_scanner_id = pair[not known_scanner_pair_idx]
                    is_found = True
                    break
            if is_found:
                break
        
        # Find the location of the other scanner
        # print("CHECKING", pair)

        # Generate a mapping between the results of the scanners
        scanner1_dists = scanners_coord_dist[known_scanner_id]
        scanner2_dists = scanners_coord_dist[unknown_scanner_id]
        coord_mapping = dict()
        for coord1, scanner1_coord_dists in enumerate(scanner1_dists):
            for coord2, scanner2_coord_dists in enumerate(scanner2_dists):
                num_dist_overlap = num_overlapping_dists(scanner1_coord_dists, scanner2_coord_dists)
                if num_dist_overlap >= 11:
                    # print("------------------")
                    # print(pair)
                    # print(coord1, coord2, num_dist_overlap)
                    coord_mapping[coord1] = coord2
        # print(coord_mapping)

        # Find the location of the scanner
   
        face_py_up1 = lambda coord: coord
        face_py_up2 = lambda coord: (-coord[2], coord[1], coord[0])
        face_py_up3 = lambda coord: (-coord[0], coord[1], -coord[2])
        face_py_up4 = lambda coord: (coord[2], coord[1], -coord[0])


        face_nx_up1 = lambda coord: (-coord[1], coord[0], coord[2])
        face_nx_up2 = lambda coord: (-coord[1], -coord[2], coord[0])
        face_nx_up3 = lambda coord: (-coord[1], -coord[0], -coord[2])
        face_nx_up4 = lambda coord: (-coord[1], coord[2], -coord[0])


        face_px_up1 = lambda coord: (coord[1], -coord[0], coord[2])
        face_px_up2 = lambda coord: (coord[1], coord[2], coord[0])
        face_px_up3 = lambda coord: (coord[1], -coord[2], -coord[0])
        face_px_up4 = lambda coord: (coord[1], coord[0], -coord[2])


        face_ny_up1 = lambda coord: (-coord[0], -coord[1], coord[2])
        face_ny_up2 = lambda coord: (coord[2], -coord[1], coord[0])
        face_ny_up3 = lambda coord: (coord[0], -coord[1], -coord[2])
        face_ny_up4 = lambda coord: (-coord[2], -coord[1], -coord[0])


        face_pz_up1 = lambda coord: (coord[0], -coord[2], coord[1])
        face_pz_up2 = lambda coord: (coord[2], coord[0], coord[1])
        face_pz_up3 = lambda coord: (-coord[0], coord[2], coord[1])
        face_pz_up4 = lambda coord: (-coord[2], -coord[0], coord[1])


        face_nz_up1 = lambda coord: (coord[0], coord[2], -coord[1])
        face_nz_up2 = lambda coord: (-coord[2], coord[0], -coord[1])
        face_nz_up3 = lambda coord: (-coord[0], -coord[2], -coord[1])
        face_nz_up4 = lambda coord: (coord[2], -coord[0], -coord[1])


        
        operations = [
            face_py_up1, face_py_up2, face_py_up3, face_py_up4, 
            face_nx_up1, face_nx_up2, face_nx_up3, face_nx_up4, 
            face_px_up1, face_px_up2, face_px_up3, face_px_up4, 
            face_ny_up1, face_ny_up2, face_ny_up3, face_ny_up4,
            face_pz_up1, face_pz_up2, face_pz_up3, face_pz_up4,
            face_nz_up1, face_nz_up2, face_nz_up3, face_nz_up4,
            ]



        for i, op in enumerate(operations):
            op_arr = lambda coord: np.array(op(coord), dtype=int)
            scanner_possible_loc = None
            is_found = True
            for known_beacon_idx1 in coord_mapping.keys():
                known_beacon_idx2 = coord_mapping[known_beacon_idx1]

                beacon_coord1 = scanners[known_scanner_id][known_beacon_idx1]
                beacon_coord2 = scanners[unknown_scanner_id][known_beacon_idx2]

                scanner_possible_loc_comp =  beacon_coord1 - np.array(op(beacon_coord2), dtype=int)

                if scanner_possible_loc is None:
                    scanner_possible_loc =  scanner_possible_loc_comp
            
                else:
                    if tuple(scanner_possible_loc) != tuple(scanner_possible_loc_comp):
                        # print(scanner_possible_loc, scanner_possible_loc_comp)
                        # print(f"Operation {op} not correct")
                        is_found = False
                        break
            if is_found is True:
                # print("FOUND scanner 2", scanner_possible_loc)
                break
                
        assert is_found is not False


        # Add the newly located scanner to the known scanners 
        known_scanners[unknown_scanner_id] = scanner_possible_loc


        # Recalculate the beacon locations of the newly located scanner
        for i, beacon in enumerate(scanners[unknown_scanner_id]):
            scanners[unknown_scanner_id][i] = scanner_possible_loc + op_arr(beacon)
            beacon_locations.add(tuple(scanners[unknown_scanner_id][i]))




    num_beacons = len(beacon_locations)
    print(f"{num_beacons=}")
    print()


    print("Part 2")
    manhatten_distances = []
    for i1, scanner1_loc in enumerate(known_scanners.values()):
        for i2, scanner2_loc in enumerate(known_scanners.values()): 
            if i1 != i2:
                manhatten_distances.append(np.linalg.norm(scanner1_loc - scanner2_loc, ord=1))

    largest_distance = int(max(manhatten_distances))
    print(f"{largest_distance=}")





def part2(input_file):
    print("Part 2")
    x = read_file(input_file)


if __name__ == "__main__":
    puzzle("./input")
    print()
    # part2("./test_input")
