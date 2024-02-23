from wire import *
from mux import *
from cmp import *


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
    neg_out.assume(ZERO if initial == ONE else ONE)
    wire_out.assume(initial)


def DFlipFlop(circuit, wire_clk, wire_data, wire_out, initial):
    neg_clk = circuit.new_wire()
    Not(circuit, wire_clk, neg_clk)
    inter = circuit.new_wire()
    DLatch(circuit, wire_clk, wire_data, inter, initial)
    DLatch(circuit, neg_clk, inter, wire_out, initial)


class Reg8:
    def snapshot(self):
        val = 0
        for i in range(8):
            d = self.wires_out[i].get()
            if d == ONE:
                val += 2**i
            elif d == ZERO:
                pass
            else:
                return "X"
        return val

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
        cells = []
        for i in range(256):
            cells.append(self.regs[i].snapshot())
        return cells

    def __init__(
        self, circuit, wire_clk, wire_write, wires_addr, wires_data, wires_out, initial
    ):
        self.regs = []
        regs_outs = [list() for _ in range(8)]
        for i in range(256):
            wires = []
            cell_addr = []
            byte = i
            for bit in range(8):
                w = circuit.new_wire()
                wires.append(w)
                regs_outs[bit].append(w)
                if byte % 2 == 0:
                    cell_addr.append(circuit.zero())
                else:
                    cell_addr.append(circuit.one())
                byte //= 2
            is_sel = circuit.new_wire()
            is_wr = circuit.new_wire()
            is_wr_clk = circuit.new_wire()
            Equals8(circuit, wires_addr, cell_addr, is_sel)
            And(circuit, is_sel, wire_write, is_wr)
            And(circuit, is_wr, wire_clk, is_wr_clk)
            self.regs.append(Reg8(circuit, is_wr_clk, wires_data, wires, initial[i]))

        for i in range(8):
            Mux8x256(circuit, wires_addr, regs_outs[i], wires_out[i])
