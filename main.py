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
        print("RAM:", self.ram.snapshot())

    def __init__(self, wire_clk, wires_out):
        zero = [Wire.zero()] * 8
        one = [Wire.one()] + [Wire.zero()] * 7
        min_one = [Wire.one()] * 8

        pc_out = [Wire() for _ in range(8)]
        pc_inc = [Wire() for _ in range(8)]
        self.inc = Adder8(pc_out, one, Wire.zero(), pc_inc, Wire())

        p_out = [Wire() for _ in range(8)]
        p_inc = [Wire() for _ in range(8)]
        p_dec = [Wire() for _ in range(8)]
        self.p_inc_gate = Adder8(p_out, one, Wire.zero(), p_inc, Wire())
        self.p_dec_gate = Adder8(p_out, min_one, Wire.zero(), p_dec, Wire())

        data = [Wire() for _ in range(8)]
        data_inc = [Wire() for _ in range(8)]
        data_dec = [Wire() for _ in range(8)]
        is_data_zero = Wire()
        is_data_not_zero = Wire()
        self.mem_inc_gate = Adder8(data, one, Wire.zero(), data_inc, Wire())
        self.mem_dec_gate = Adder8(data, min_one, Wire.zero(), data_dec, Wire())
        self.is_data_zero_gate = Equals8(data, zero, is_data_zero)
        self.is_data_not_zero_gate = Not(is_data_zero, is_data_not_zero)

        instruction = [Wire() for _ in range(8)]

        is_fwd = Wire()
        is_bwd = Wire()
        is_inc = Wire()
        is_dec = Wire()
        is_jmp = Wire()

        pc_next = [Wire() for _ in range(8)]
        p_next = [Wire() for _ in range(8)]

        is_jmp_not_zero = Wire()
        self.is_jmp_not_zero_gate = And(is_jmp, is_data_not_zero, is_jmp_not_zero)

        self.pc_calc = Mux1x2Byte(
            is_jmp_not_zero, pc_inc, instruction[3:8] + [Wire.zero()] * 3, pc_next
        )

        p_inter = [Wire() for _ in range(8)]
        is_fwd_bwd = Wire()
        self.is_fwd_bwd_gate = Or(is_fwd, is_bwd, is_fwd_bwd)

        self.p_inter_calc = Mux1x2Byte(is_bwd, p_inc, p_dec, p_inter)
        self.p_calc = Mux1x2Byte(is_fwd_bwd, p_out, p_inter, p_next)

        is_wr = Wire()
        self.is_wr_gate = Or(is_inc, is_dec, is_wr)

        data_next = [Wire() for _ in range(8)]
        self.mem_inter_calc = Mux1x2Byte(is_dec, data_inc, data_dec, data_next)

        self.pc = Reg8(wire_clk, pc_next, pc_out)
        self.p = Reg8(wire_clk, p_next, p_out)
        self.rom = RAM(wire_clk, Wire.zero(), pc_out, zero, instruction)
        self.ram = RAM(wire_clk, is_wr, p_out, data_next, data)

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
        self.rom.fill([2, 2, 2, 2, 2, 2, 2, 3, 4 + (7 << 3)] + [0 for i in range(248)])

    def update(self):
        self.pc.update()
        self.p.update()
        self.inc.update()
        self.p_inc_gate.update()
        self.p_dec_gate.update()
        self.rom.update()
        self.ram.update()
        self.is_fwd_check.update()
        self.is_bwd_check.update()
        self.is_inc_check.update()
        self.is_dec_check.update()
        self.is_jmp_check.update()

        self.is_fwd_bwd_gate.update()
        self.p_inter_calc.update()
        self.p_calc.update()
        self.is_data_zero_gate.update()
        self.is_data_not_zero_gate.update()
        self.is_jmp_not_zero_gate.update()
        self.pc_calc.update()
        self.is_wr_gate.update()
        self.mem_inc_gate.update()
        self.mem_dec_gate.update()
        self.mem_inter_calc.update()


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

        circuit.snapshot()
        clk_val = not clk_val
