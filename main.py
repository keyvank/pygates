#!/usr/bin/python3

import time

from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *


class Circuit:
    def __init__(self, wire_clk, wires_out):
        data = [Wire.zero()] * 8
        one = [Wire.one()] + [Wire.zero()] * 7

        a_output = [Wire() for _ in range(8)]
        self.reg_a = Reg8(Wire.zero(), data, a_output)

        b_output = [Wire() for _ in range(8)]
        self.reg_b = Reg8(Wire.zero(), data, b_output)

        a_plus_b_out = [Wire() for _ in range(8)]
        self.a_plus_b = Adder8(a_output, b_output, Wire.zero(), a_plus_b_out, Wire())

        pc_out = [Wire() for _ in range(8)]
        pc_next = [Wire() for _ in range(8)]
        self.inc = Adder8(pc_out, one, Wire.zero(), pc_next, Wire())

        self.pc = Reg8(wire_clk, pc_next, pc_out)
        self.memory = RAM(Wire.zero(), pc_out, data, wires_out)

        # Pre-fill memory
        self.memory.fill([(i) % 256 for i in range(256)])

    def update(self):
        self.pc.update()
        self.inc.update()
        self.memory.update()


if __name__ == "__main__":
    clk = Wire()
    clk_val = False

    outs = [Wire() for _ in range(8)]
    circuit = Circuit(clk, outs)

    while True:
        if clk_val:
            clk.put(BATTERY, ONE)
        else:
            clk.put(BATTERY, ZERO)
        circuit.update()
        time.sleep(0.05)

        print(clk.get(), [out.get() for out in outs])
        clk_val = not clk_val
