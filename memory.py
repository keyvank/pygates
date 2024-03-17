from wire import *
from mux import *
from cmp import *
from utils import wires_to_num, num_to_wires


def DLatch(circuit, in_clk, in_data, out_data, initial=0):
    not_data = circuit.new_wire()
    Not(circuit, in_data, not_data)
    and_d_clk = circuit.new_wire()
    And(circuit, in_data, in_clk, and_d_clk)
    and_notd_clk = circuit.new_wire()
    And(circuit, not_data, in_clk, and_notd_clk)
    neg_out = circuit.new_wire()
    Nor(circuit, and_notd_clk, neg_out, out_data)
    Nor(circuit, and_d_clk, out_data, neg_out)

    neg_out.assume(1 - initial)
    out_data.assume(initial)


def DFlipFlop(circuit, in_clk, in_data, out_data, initial=0):
    neg_clk = circuit.new_wire()
    Not(circuit, in_clk, neg_clk)
    inter = circuit.new_wire()
    DLatch(circuit, in_clk, in_data, inter, initial)
    DLatch(circuit, neg_clk, inter, out_data, initial)


class Reg8:
    def snapshot(self):
        return wires_to_num(self.out_data)

    def __init__(self, circuit, in_clk, in_data, out_data, initial=0):
        self.out_data = out_data
        for i in range(8):
            DFlipFlop(
                circuit,
                in_clk,
                in_data[i],
                out_data[i],
                ZERO if initial % 2 == 0 else ONE,
            )
            initial //= 2


class RAM:
    def snapshot(self):
        return [self.regs[i].snapshot() for i in range(256)]

    def __init__(self, circuit, in_clk, in_wr, in_addr, in_data, out_data, initial):
        self.regs = []
        reg_outs = [[circuit.new_wire() for _ in range(8)] for _ in range(256)]

        for i in range(256):
            is_sel = circuit.new_wire()
            MultiEquals(circuit, in_addr, num_to_wires(circuit, i), is_sel)
            is_wr = circuit.new_wire()
            And(circuit, is_sel, in_wr, is_wr)
            is_wr_and_clk = circuit.new_wire()
            And(circuit, is_wr, in_clk, is_wr_and_clk)
            self.regs.append(
                Reg8(circuit, is_wr_and_clk, in_data, reg_outs[i], initial[i])
            )

        for i in range(8):
            Mux8x256(
                circuit, in_addr, [reg_outs[j][i] for j in range(256)], out_data[i]
            )


class FastRAM:
    def snapshot(self):
        return self.data

    def __init__(self, circuit, in_clk, in_wr, in_addr, in_data, out_data, initial):
        self.in_clk = in_clk
        self.in_wr = in_wr
        self.in_addr = in_addr
        self.in_data = in_data
        self.out_data = out_data
        self.data = initial
        self.clk_is_up = False
        circuit.add_component(self)

    def update(self):
        clk = self.in_clk.get()
        addr = wires_to_num(self.in_addr)
        data = wires_to_num(self.in_data)
        if clk == ZERO and self.clk_is_up:
            wr = self.in_wr.get()
            if wr == ONE:
                self.data[addr] = data
            self.clk_is_up = False
        elif clk == ONE:
            self.clk_is_up = True

        value = self.data[addr]
        for i in range(8):
            self.out_data[i].put(self, ONE if (value >> i) & 1 else ZERO)

        return False
