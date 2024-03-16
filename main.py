#!/usr/bin/python3

import time

from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *
from circuit import *

c = Circuit()
a = Wire.zero()
b = Wire.zero()
o = c.new_wire()
Xor(c, a, b, o)
c.update()
print(o.get())
# exit(0)
# print(c._transistors.__len__())
# exit(0)


def Mux1x2Byte(circuit, wire_select, wires_data_a, wires_data_b, wires_out):
    for i in range(8):
        Mux1x2(
            circuit,
            [wire_select],
            [wires_data_a[i], wires_data_b[i]],
            wires_out[i],
        )


class ProgramCounter:
    def snapshot(self):
        print("Program Counter:", self.pc.snapshot())

    def __init__(self, circuit, wire_clk, wires_out):
        one = [circuit.one()] + [circuit.zero()] * 7
        pc_out = [circuit.new_wire() for _ in range(8)]
        self.pc_inc = [circuit.new_wire() for _ in range(8)]
        Adder8(circuit, pc_out, one, circuit.zero(), self.pc_inc, circuit.new_wire())
        self.pc = Reg8(circuit, wire_clk, self.pc_inc, pc_out, 0)


class ProgramReader:
    def snapshot(self):
        print("Program Counter:", self.pc.snapshot())
        print("Instruction:", [w.get() for w in self.instruction])

    def __init__(self, circuit, wire_clk, wires_out):
        one = [circuit.one()] + [circuit.zero()] * 7
        pc_out = [circuit.new_wire() for _ in range(8)]
        self.instruction = [circuit.new_wire() for _ in range(8)]
        self.pc_inc = [circuit.new_wire() for _ in range(8)]
        Adder8(circuit, pc_out, one, circuit.zero(), self.pc_inc, circuit.new_wire())
        self.pc = Reg8(circuit, wire_clk, self.pc_inc, pc_out, 0)
        self.rom = RAM(
            circuit,
            wire_clk,
            circuit.zero(),
            pc_out,
            [circuit.zero()] * 8,
            self.instruction,
            [i * 2 for i in range(256)],
        )


class CPU:
    def snapshot(self):
        print("P:", self.p.snapshot())
        print("PC:", self.pc.snapshot())
        print("RAM:", self.ram.snapshot())

    def __init__(self, circuit, wire_clk, wires_out):
        zero = [circuit.zero()] * 8
        one = [circuit.one()] + [circuit.zero()] * 7
        min_one = [circuit.one()] * 8
        pc_out = [circuit.new_wire() for _ in range(8)]
        pc_inc = [circuit.new_wire() for _ in range(8)]
        p_out = [circuit.new_wire() for _ in range(8)]
        p_inc = [circuit.new_wire() for _ in range(8)]
        p_dec = [circuit.new_wire() for _ in range(8)]
        data = [circuit.new_wire() for _ in range(8)]
        data_inc = [circuit.new_wire() for _ in range(8)]
        data_dec = [circuit.new_wire() for _ in range(8)]
        is_data_zero = circuit.new_wire()
        is_data_not_zero = circuit.new_wire()
        instruction = [circuit.new_wire() for _ in range(8)]
        is_fwd = circuit.new_wire()
        is_bwd = circuit.new_wire()
        is_inc = circuit.new_wire()
        is_dec = circuit.new_wire()
        is_jmp = circuit.new_wire()
        pc_next = [circuit.new_wire() for _ in range(8)]
        p_next = [circuit.new_wire() for _ in range(8)]
        is_jmp_not_zero = circuit.new_wire()
        p_inter = [circuit.new_wire() for _ in range(8)]
        is_fwd_bwd = circuit.new_wire()
        is_wr = circuit.new_wire()
        data_next = [circuit.new_wire() for _ in range(8)]

        Adder8(circuit, pc_out, one, circuit.zero(), pc_inc, circuit.new_wire())
        Adder8(circuit, p_out, one, circuit.zero(), p_inc, circuit.new_wire())
        Adder8(circuit, p_out, min_one, circuit.zero(), p_dec, circuit.new_wire())
        Adder8(circuit, data, one, circuit.zero(), data_inc, circuit.new_wire())
        Adder8(circuit, data, min_one, circuit.zero(), data_dec, circuit.new_wire())
        MultiEquals(circuit, data, zero, is_data_zero)
        Not(circuit, is_data_zero, is_data_not_zero)
        And(circuit, is_jmp, is_data_not_zero, is_jmp_not_zero)
        Mux1x2Byte(
            circuit,
            is_jmp_not_zero,
            pc_inc,
            instruction[1:8] + [circuit.zero()],
            pc_next,
        )

        Or(circuit, is_fwd, is_bwd, is_fwd_bwd)
        Mux1x2Byte(circuit, is_bwd, p_inc, p_dec, p_inter)
        Mux1x2Byte(circuit, is_fwd_bwd, p_out, p_inter, p_next)
        Or(circuit, is_inc, is_dec, is_wr)
        Mux1x2Byte(circuit, is_dec, data_inc, data_dec, data_next)

        self.pc = Reg8(circuit, wire_clk, pc_next, pc_out, 0)
        self.p = Reg8(circuit, wire_clk, p_next, p_out, 0)

        self.rom = RAM(
            circuit,
            wire_clk,
            circuit.zero(),
            pc_out,
            zero,
            instruction,
            compile("+>+[[->+>+<<]>[-<+>]<<[->>+>+<<<]>>[-<<+>>]>[-<+>]<]"),
        )
        self.ram = RAM(
            circuit, wire_clk, is_wr, p_out, data_next, data, [0 for _ in range(256)]
        )
        MultiEquals(
            circuit,
            instruction[0:3],
            [circuit.zero(), circuit.zero(), circuit.zero()],
            is_fwd,
        )
        MultiEquals(
            circuit,
            instruction[0:3],
            [circuit.zero(), circuit.one(), circuit.zero()],
            is_bwd,
        )
        MultiEquals(
            circuit,
            instruction[0:3],
            [circuit.zero(), circuit.zero(), circuit.one()],
            is_inc,
        )
        MultiEquals(
            circuit,
            instruction[0:3],
            [circuit.zero(), circuit.one(), circuit.one()],
            is_dec,
        )
        Equals(circuit, instruction[0], circuit.one(), is_jmp)


def compile(bf):
    opcodes = []
    locs = []

    for c in bf:
        if c == ">":
            opcodes.append(0)
        elif c == "<":
            opcodes.append(2)
        elif c == "+":
            opcodes.append(4)
        elif c == "-":
            opcodes.append(6)
        elif c == "[":
            locs.append(len(opcodes))
        elif c == "]":
            opcodes.append(1 + (locs.pop() << 1))

    return opcodes + [0 for _ in range(256 - len(opcodes))]


if __name__ == "__main__":
    circ = Circuit()
    clk = circ.new_wire()
    clk.put(BATTERY, ZERO)
    clk_val = False

    outs = [circ.new_wire() for _ in range(8)]
    cpu = ProgramReader(circ, clk, outs)
    print(circ._transistors.__len__())
    while True:
        circ.stabilize()
        cpu.snapshot()
        if clk_val:
            clk.put(BATTERY, ONE)
        else:
            clk.put(BATTERY, ZERO)
        clk_val = not clk_val
