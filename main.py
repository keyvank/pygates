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
    def snapshot(self):
        print("P:", self.p.snapshot())
        print("PC:", self.pc.snapshot())

    def __init__(self, wire_clk, wires_out):
        data = [Wire.zero()] * 8
        one = [Wire.one()] + [Wire.zero()] * 7
        min_one = [Wire.one()] * 8

        a_output = [Wire() for _ in range(8)]
        self.reg_a = Reg8(Wire.zero(), data, a_output)

        b_output = [Wire() for _ in range(8)]
        self.reg_b = Reg8(Wire.zero(), data, b_output)

        a_plus_b_out = [Wire() for _ in range(8)]
        self.a_plus_b = Adder8(a_output, b_output, Wire.zero(), a_plus_b_out, Wire())

        pc_out = [Wire() for _ in range(8)]
        pc_inc = [Wire() for _ in range(8)]
        self.inc = Adder8(pc_out, one, Wire.zero(), pc_inc, Wire())

        p_out = [Wire() for _ in range(8)]
        p_inc = [Wire() for _ in range(8)]
        p_dec = [Wire() for _ in range(8)]
        self.p_inc_gate = Adder8(p_out, one, Wire.zero(), p_inc, Wire())
        self.p_dec_gate = Adder8(p_out, min_one, Wire.zero(), p_dec, Wire())

        instruction = [Wire() for _ in range(8)]

        is_fwd = Wire()
        is_bwd = Wire()
        is_inc = Wire()
        is_dec = Wire()
        is_jmp = Wire()

        pc_next = [Wire() for _ in range(8)]
        p_next = [Wire() for _ in range(8)]

        self.dec = Mux1x2Byte(
            is_jmp, pc_inc, [Wire.zero()] * 3 + instruction[3:8], pc_next
        )

        self.pc = Reg8(wire_clk, pc_next, pc_out)
        self.p = Reg8(wire_clk, p_dec, p_out)
        self.memory = RAM(Wire.zero(), pc_out, data, instruction)

        self.is_fwd_check = Equals3(
            instruction[0:3], [Wire.zero(), Wire.zero(), Wire.zero()], is_fwd
        )
        self.is_bwd_check = Equals3(
            instruction[0:3], [Wire.one(), Wire.zero(), Wire.zero()], is_bwd
        )
        self.is_inc_check = Equals3(
            instruction[0:3], [Wire.zero(), Wire.one(), Wire.zero()], is_inc
        )
        self.is_dec_check = Equals3(
            instruction[0:3], [Wire.one(), Wire.one(), Wire.zero()], is_dec
        )
        self.is_jmp_check = Equals3(
            instruction[0:3], [Wire.zero(), Wire.zero(), Wire.one()], is_jmp
        )

        # Pre-fill memory
        self.memory.fill([4 + (30 << 3) if i == 3 else 0 for i in range(256)])

    def update(self):
        self.pc.update()
        self.p.update()
        self.inc.update()
        self.p_inc_gate.update()
        self.p_dec_gate.update()
        self.memory.update()
        self.is_fwd_check.update()
        self.is_bwd_check.update()
        self.is_inc_check.update()
        self.is_dec_check.update()
        self.is_jmp_check.update()
        self.dec.update()


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

        circuit.snapshot()
        clk_val = not clk_val
