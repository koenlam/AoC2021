#! /usr/bin/env python3
from functools import reduce
import numpy as np

def read_file(filename):
    with open(filename) as f:
        return f.read().strip()


def lpad(str, length):
    return "0"*(length - len(str)) + str


def convert2binary(hex_nums):
    bin_num = ""
    for hex_num in hex_nums:
        bin_num += lpad(bin(int(f"0x{hex_num}", 16))[2:], 4)
    return bin_num

def parse_header(packet):
    packet_version = int(packet[:3],2)
    type_id = int(packet[3:6], 2)
    return packet_version, type_id


def parse_packet_versions(packet):
    packet_version, type_id = parse_header(packet)
    packet_version_sum = packet_version

    packet = packet[6:] # Remove the packet header from the packet
    if type_id == 4:
        # Literal value

        # Skip until the last packet
        num_groups = 0
        # print("HERE", packet)
        while packet[0] != '0':
            # print("HERE2", packet)
            packet = packet[5:]
            num_groups += 1
        num_groups += 1
    
        total_packet_len = 6 + num_groups*5
        # print("PACKET lEN", total_packet_len)

        return total_packet_len, packet_version

    else:
        # Some operator
        
        # Parse the smaller packets
        length_type_ID = packet[:1]
        packet = packet[1:]
        if length_type_ID == '0':
            # Next 15 bits represets the total length in bits of the sub-packets
            total_length_subpackets = int(packet[:15], 2) 
            packet = packet[15:] 

            # return [packet_version] + parse_packet(packet[:total_length_subpackets])

            subpacket_parsed_len = 0
            while subpacket_parsed_len != total_length_subpackets:
                # print("TYPE 0", subpacket_parsed_len, total_length_subpackets)
                if subpacket_parsed_len > total_length_subpackets:
                    raise ValueError(f"Packet length incorrectly parsed")
                # print(packet)
                subpacket_len, subpacket_version =  parse_packet_versions(packet)
                packet = packet[subpacket_len:]
                subpacket_parsed_len += subpacket_len
                packet_version_sum += subpacket_version
            
            total_packet_parsed = 6 + 1 + 15 + subpacket_parsed_len
            return total_packet_parsed, packet_version_sum
                
        elif length_type_ID == '1':
            # Next 11 bits represents the number of sub-packets immediately contained
            num_subpackets = int(packet[:11], 2)
            packet = packet[11:]

            subpacket_parsed_len = 0
            for i in range(num_subpackets):
                # print("TYPE 1", i, num_subpackets)
                # print(packet)
                subpacket_len, subpacket_version =  parse_packet_versions(packet)
                packet = packet[subpacket_len:]
                subpacket_parsed_len += subpacket_len
                packet_version_sum += subpacket_version

            total_packet_parsed = 6 + 1 + 11 + subpacket_parsed_len
            return total_packet_parsed, packet_version_sum




def part1(input_file):
    print("Part 1")
    transmission_hex = read_file(input_file)
    transmission_bin = convert2binary(transmission_hex)
    version_sum = parse_packet_versions(transmission_bin)[0]
    print(f"{version_sum=}")



def parse_packet(packet):
    packet_version, type_id = parse_header(packet)

    packet = packet[6:] # Remove the packet header from the packet
    if type_id == 4:
        # Literal value

        num_groups = 0
        literal_bin = ""
        while packet[0] != '0':
            # print("HERE2", packet)
            literal_bin += packet[1:5]
            packet = packet[5:]

            num_groups += 1
        num_groups += 1
        literal_bin += packet[1:5]
        literal_num = int(literal_bin, 2)    
        total_packet_len = 6 + num_groups*5
        return total_packet_len, literal_num

    else:
        # Some operator
        product = lambda l: reduce(lambda a,b: a*b, l)
        greater = lambda l: 1 if l[0] > l[1] else 0
        less = lambda l: 1 if l[0] < l[1] else 0
        equal = lambda l: 1 if l[0] == l[1] else 0

        operators = {
            0: sum,
            1: product,
            2: min,
            3: max,
            5: greater,
            6: less,
            7: equal,
        }
        
        operator = operators[type_id]
        
        # Parse the smaller packets
        length_type_ID = packet[:1]
        packet = packet[1:]
        if length_type_ID == '0':
            # Next 15 bits represets the total length in bits of the sub-packets
            total_length_subpackets = int(packet[:15], 2) 
            packet = packet[15:] 

            subpacket_values = []
            subpacket_parsed_len = 0
            while subpacket_parsed_len != total_length_subpackets:
                # print("TYPE 0", subpacket_parsed_len, total_length_subpackets)
                if subpacket_parsed_len > total_length_subpackets:
                    raise ValueError(f"Packet length incorrectly parsed")
                subpacket_len, subpacket_value =  parse_packet(packet)
                packet = packet[subpacket_len:]
                subpacket_parsed_len += subpacket_len
                subpacket_values.append(subpacket_value)
            
            total_packet_parsed = 6 + 1 + 15 + subpacket_parsed_len
            return total_packet_parsed, operator(subpacket_values)
                
        elif length_type_ID == '1':
            # Next 11 bits represents the number of sub-packets immediately contained
            num_subpackets = int(packet[:11], 2)
            packet = packet[11:]

            subpacket_values = []
            subpacket_parsed_len = 0
            for i in range(num_subpackets):
                # print("TYPE 1", i, num_subpackets)
                subpacket_len, subpacket_value =  parse_packet(packet)
                packet = packet[subpacket_len:]
                subpacket_parsed_len += subpacket_len
                subpacket_values.append(subpacket_value)

            total_packet_parsed = 6 + 1 + 11 + subpacket_parsed_len
            return total_packet_parsed, operator(subpacket_values)



def part2(input_file):
    print("Part 2")
    transmission_hex = read_file(input_file)
    transmission_bin = convert2binary(transmission_hex)
    result = parse_packet(transmission_bin)[0]
    print(f"{result=}")


if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
