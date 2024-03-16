from wire import *
from mux import *
from cmp import *
from utils import wires_to_num, num_to_wires


def DLatch(circuit, wire_clk, wire_data, wire_out, initial):
    not_data = circuit.new_wire()
    Not(circuit, wire_data, not_data)
    and_d_clk = circuit.new_wire()
    And(circuit, wire_data, wire_clk, and_d_clk)
    and_notd_clk = circuit.new_wire()
    And(circuit, not_data, wire_clk, and_notd_clk)
    neg_out = circuit.new_wire()
    Nor(circuit, and_notd_clk, neg_out, wire_out)
    Nor(circuit, and_d_clk, wire_out, neg_out)

    neg_out.assume(1 - initial)
    wire_out.assume(initial)


def DFlipFlop(circuit, wire_clk, wire_data, wire_out, initial):
    neg_clk = circuit.new_wire()
    Not(circuit, wire_clk, neg_clk)
    inter = circuit.new_wire()
    DLatch(circuit, wire_clk, wire_data, inter, initial)
    DLatch(circuit, neg_clk, inter, wire_out, initial)


class Reg8:
    def snapshot(self):
        return wires_to_num(self.wires_out)

    def __init__(self, circuit, wire_clk, wires_data, wires_out, initial):
        self.wires_out = wires_out
        for i in range(8):
            DFlipFlop(
                circuit,
                wire_clk,
                wires_data[i],
                wires_out[i],
                ZERO if initial % 2 == 0 else ONE,
            )
            initial //= 2


class RAM:
    def snapshot(self):
        return [self.regs[i].snapshot() for i in range(256)]

    def __init__(
        self, circuit, wire_clk, wire_write, wires_addr, wires_data, wires_out, initial
    ):
        self.regs = []
        reg_outs = [[circuit.new_wire() for _ in range(8)] for _ in range(256)]

        for i in range(256):
            is_sel = circuit.new_wire()
            MultiEquals(circuit, wires_addr, num_to_wires(circuit, i), is_sel)
            is_wr = circuit.new_wire()
            And(circuit, is_sel, wire_write, is_wr)
            is_wr_and_clk = circuit.new_wire()
            And(circuit, is_wr, wire_clk, is_wr_and_clk)
            self.regs.append(
                Reg8(circuit, is_wr_and_clk, wires_data, reg_outs[i], initial[i])
            )

        for i in range(8):
            Mux8x256(
                circuit, wires_addr, [reg_outs[j][i] for j in range(256)], wires_out[i]
            )


class FastRAM:
    def snapshot(self):
        return self.data

    def __init__(
        self, circuit, wire_clk, wire_write, wires_addr, wires_data, wires_out, initial
    ):
        self.wire_clk = wire_clk
        self.wire_write = wire_write
        self.wires_addr = wires_addr
        self.wires_data = wires_data
        self.wires_out = wires_out
        self.data = initial
        self.clk_is_up = False
        circuit.add_component(self)

    def update(self):
        clk = self.wire_clk.get()
        addr = wires_to_num(self.wires_addr)
        data = wires_to_num(self.wires_data)
        if clk == ZERO and self.clk_is_up:
            wr = self.wire_write.get()
            if wr == ONE:
                self.data[addr] = data
            self.clk_is_up = False
        elif clk == ONE:
            self.clk_is_up = True

        value = self.data[addr]
        for i in range(8):
            self.wires_out[i].put(self, ONE if (value >> i) & 1 else ZERO)

        return False
