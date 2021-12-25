#! /usr/bin/env python3
import re
import numpy as np

from collections import defaultdict
from functools import reduce
from copy import deepcopy


def read_file(filename):
    with open(filename) as f:
        return f.read().strip().split("\n")


class InputNumber:
    def __init__(self, input_number):
        self.input_number = str(input_number)
        self.idx = 0

    def get(self):
        if self.idx >= len(self.input_number):
            raise IndexError(f"{self.idx=}, {len(self.input_number)}")

        n = self.input_number[self.idx]
        # print(n)
        self.idx += 1
        return int(n)


class ALU:
    def __init__(self, input_number=None):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input_number = input_number

    def parse_val(self, val):
        if val == "w":
            return self.w
        elif val == "x":
            return self.x
        elif val == "y":
            return self.y
        elif val == "z":
            return self.z
        else:
            return int(val)

    
    def set_input(self, var, val):
        if var == "w":
            self.w = val
        elif var == "x":
            self.x = val
        elif var == "y":
            self.y = val
        elif var == "z":
            self.z = val
        else:
            raise ValueError(f"{var=} is invalid")


    def run(self, opcode, vals):
        if opcode == "inp":
            assert len(vals) == 1
            self.inp(vals[0])
        elif opcode == "add":
            assert len(vals) == 2
            self.add(vals[0], vals[1])
        elif opcode == "mul":
            assert len(vals) == 2
            self.mul(vals[0], vals[1])
        elif opcode == "div":
            assert len(vals) == 2
            self.div(vals[0], vals[1])
        elif opcode == "mod":
            assert len(vals) == 2
            self.mod(vals[0], vals[1])
        elif opcode == "mul":
            assert len(vals) == 2
            self.mul(vals[0], vals[1])
        elif opcode == "eql":
            assert len(vals) == 2
            self.eql(vals[0], vals[1])
        else:
            raise ValueError(f"{opcode=} is invalid")

    def inp(self, var):
        self.set_input(var, self.input_number.get())


    def add(self, var1, var2):
        res = self.parse_val(var1) + self.parse_val(var2)
        self.set_input(var1, res)


    def mul(self, var1, var2):
        res = self.parse_val(var1) * self.parse_val(var2)
        self.set_input(var1, res)

    def div(self, var1, var2):
        res = self.parse_val(var1) // self.parse_val(var2)
        self.set_input(var1, res)

    def mod(self, var1, var2):
        res = self.parse_val(var1) % self.parse_val(var2)
        self.set_input(var1, res)


    def eql(self, var1, var2):
        res = int(self.parse_val(var1) == self.parse_val(var2))
        self.set_input(var1, res)

    def print_alu(self):
        print(f"{self.w=}")
        print(f"{self.x=}")
        print(f"{self.y=}")
        print(f"{self.z=}")



class MONAD:
    def __init__(self):
        self.counter = 1
        self.z = 0
    
    def gen_possible_w(self):
        if self.counter not in [4,6,8,9,10,13,14]:
            return range(9,0,-1)
        else:
            adds = {4: -3, 6:-9, 8:-7, 9:-11, 10:-4, 13:-8, 14:-10}
            add = adds[self.counter]
            w = (self.z % 26) + add
            return [w] if w in range(1,10) else []


    def run(self, w):
        if self.counter in [4,6,8,9,10,13,14]:
            self.z = self.z // 26
        else:
            adds = {1: 7, 2:15, 3:2, 5: 14, 7:15, 11: 12, 12:2}
            add = adds[self.counter]
            self.z = (self.z*26) + w + add
        self.counter += 1


def parse_instruction(instruction):
    opcode = instruction.split()[0]
    vals = instruction.split()[1:]
    return opcode, vals


def test_add():
    alu = ALU()
    alu.run("add", ["w", 10])
    assert alu.w == 10


    alu.run("add", ["w", -11])
    assert alu.w == -1


def walk(monad, instructions, num="", largest=True):
    # print(len(num), num)
    if len(num) == 14:
        # Test if it is correct
        input_number = InputNumber(num)
        alu = ALU(input_number)
        for instruction in instructions:
            opcode, vals = parse_instruction(instruction)
            alu.run(opcode, vals)
        # print(num, monad.z)
        if alu.z == 0:
            return num
        else:
            return None
    else:
        possible_w = monad.gen_possible_w()
        for w in sorted(possible_w, reverse=largest):
            monad_n = deepcopy(monad)
            monad_n.run(w)
            res = walk(monad_n, instructions, num+str(w), largest)
            if res is not None:
                return res



def part1(input_file):
    print("Part 1")
    instructions = read_file(input_file)
    monad = MONAD()
    largest_num = int(walk(monad, instructions, largest=True))
    print(f"{largest_num=}")





def part2(input_file):
    print("Part 2")
    instructions = read_file(input_file)
    # def walk(monad, num=""):
    #     # print(len(num), num)
    #     if len(num) == 14:
    #         # Test if it is correct
    #         input_number = InputNumber(num)
    #         alu = ALU(input_number)
    #         for instruction in instructions:
    #             opcode, vals = parse_instruction(instruction)
    #             alu.run(opcode, vals)
    #         # print(num, monad.z)
    #         if alu.z == 0:
    #             return num
    #         else:
    #             return None
    #     else:
    #         possible_w = monad.gen_possible_w()
    #         for w in sorted(possible_w):
    #             monad_n = deepcopy(monad)
    #             monad_n.run(w)
    #             res = walk(monad_n, num=num+str(w))
    #             if res is not None:
    #                 return res

    monad = MONAD()
    smallest_num = int(walk(monad, instructions, largest=False))
    print(f"{smallest_num=}")



if __name__ == "__main__":
    part1("./input")
    print()
    part2("./input")
