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


class Mux1x2Byte:
    def __init__(self, circuit, wire_select, wires_data_a, wires_data_b, wires_out):
        self.muxes = []
        for i in range(8):
            self.muxes.append(
                Mux1x2(
                    circuit,
                    [wire_select],
                    [wires_data_a[i], wires_data_b[i]],
                    wires_out[i],
                )
            )

    def update(self):
        for mux in self.muxes:
            mux.update()


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

        self.gates = []
        self.gates.append(
            Adder8(circuit, pc_out, one, circuit.zero(), pc_inc, circuit.new_wire())
        )
        self.gates.append(
            Adder8(circuit, p_out, one, circuit.zero(), p_inc, circuit.new_wire())
        )
        self.gates.append(
            Adder8(circuit, p_out, min_one, circuit.zero(), p_dec, circuit.new_wire())
        )
        self.gates.append(
            Adder8(circuit, data, one, circuit.zero(), data_inc, circuit.new_wire())
        )
        self.gates.append(
            Adder8(circuit, data, min_one, circuit.zero(), data_dec, circuit.new_wire())
        )
        self.gates.append(Equals8(circuit, data, zero, is_data_zero))
        self.gates.append(Not(circuit, is_data_zero, is_data_not_zero))
        self.gates.append(And(circuit, is_jmp, is_data_not_zero, is_jmp_not_zero))
        self.gates.append(
            Mux1x2Byte(
                circuit,
                is_jmp_not_zero,
                pc_inc,
                instruction[1:8] + [circuit.zero()],
                pc_next,
            )
        )

        self.gates.append(Or(circuit, is_fwd, is_bwd, is_fwd_bwd))
        self.gates.append(Mux1x2Byte(circuit, is_bwd, p_inc, p_dec, p_inter))
        self.gates.append(Mux1x2Byte(circuit, is_fwd_bwd, p_out, p_inter, p_next))
        self.gates.append(Or(circuit, is_inc, is_dec, is_wr))
        self.gates.append(Mux1x2Byte(circuit, is_dec, data_inc, data_dec, data_next))

        self.pc = Reg8(circuit, wire_clk, pc_next, pc_out)
        self.gates.append(self.pc)

        self.p = Reg8(circuit, wire_clk, p_next, p_out)
        self.gates.append(self.p)

        self.rom = RAM(circuit, wire_clk, circuit.zero(), pc_out, zero, instruction)
        self.gates.append(self.rom)

        self.ram = RAM(circuit, wire_clk, is_wr, p_out, data_next, data)
        self.gates.append(self.ram)

        self.gates.append(
            Equals3(
                circuit,
                instruction[0:3],
                [circuit.zero(), circuit.zero(), circuit.zero()],
                is_fwd,
            )
        )
        self.gates.append(
            Equals3(
                circuit,
                instruction[0:3],
                [circuit.zero(), circuit.one(), circuit.zero()],
                is_bwd,
            )
        )
        self.gates.append(
            Equals3(
                circuit,
                instruction[0:3],
                [circuit.zero(), circuit.zero(), circuit.one()],
                is_inc,
            )
        )
        self.gates.append(
            Equals3(
                circuit,
                instruction[0:3],
                [circuit.zero(), circuit.one(), circuit.one()],
                is_dec,
            )
        )
        self.gates.append(Equals(circuit, instruction[0], circuit.one(), is_jmp))

        # Pre-fill memory
        self.rom.fill(compile("+>+[[->+>+<<]>[-<+>]<<[->>+>+<<<]>>[-<<+>>]>[-<+>]<]"))

    def update(self):
        for g in self.gates:
            g.update()


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
    clk_val = False

    outs = [circ.new_wire() for _ in range(8)]
    circuit = CPU(circ, clk, outs)

    while True:
        if clk_val:
            clk.put(BATTERY, ONE)
        else:
            clk.put(BATTERY, ZERO)
        circuit.update()

        circuit.snapshot()
        clk_val = not clk_val
