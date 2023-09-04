#!/usr/bin/python3

import time

from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *


class Mux1x2Byte:
    def __init__(self, wire_select, wires_data_a, wires_data_b, wires_out):
        self.muxes = []
        for i in range(8):
            self.muxes.append(
                Mux1x2([wire_select], [wires_data_a[i], wires_data_b[i]], wires_out[i])
            )

    def update(self):
        for mux in self.muxes:
            mux.update()


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
        pc_inc = [Wire() for _ in range(8)]
        self.inc = Adder8(pc_out, one, Wire.zero(), pc_inc, Wire())

        instruction = [Wire() for _ in range(8)]

        is_inst0 = Wire()
        is_inst1 = Wire()
        is_inst2 = Wire()
        is_inst3 = Wire()

        pc_next = [Wire() for _ in range(8)]

        self.inst3 = Mux1x2Byte(is_inst3, pc_inc, pc_out, pc_next)
        self.pc = Reg8(wire_clk, pc_next, pc_out)
        self.memory = RAM(Wire.zero(), pc_out, data, instruction)

        self.is_inst0_check = Equals3(
            instruction[0:3], [Wire.zero(), Wire.zero(), Wire.zero()], is_inst0
        )
        self.is_inst1_check = Equals3(
            instruction[0:3], [Wire.one(), Wire.zero(), Wire.zero()], is_inst1
        )
        self.is_inst2_check = Equals3(
            instruction[0:3], [Wire.zero(), Wire.one(), Wire.zero()], is_inst2
        )
        self.is_inst3_check = Equals3(
            instruction[0:3], [Wire.one(), Wire.one(), Wire.zero()], is_inst3
        )

        self.conn0 = Connect(is_inst0, wires_out[0])
        self.conn1 = Connect(is_inst1, wires_out[1])
        self.conn2 = Connect(is_inst2, wires_out[2])
        self.conn3 = Connect(is_inst3, wires_out[3])

        # Pre-fill memory
        self.memory.fill([(i) % 256 for i in range(256)])

    def update(self):
        self.pc.update()
        self.inc.update()
        self.memory.update()
        self.is_inst0_check.update()
        self.is_inst1_check.update()
        self.is_inst2_check.update()
        self.is_inst3_check.update()
        self.conn0.update()
        self.conn1.update()
        self.conn2.update()
        self.conn3.update()
        self.inst3.update()


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
