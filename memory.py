from wire import *
from mux import *
from cmp import *


def DLatch(circuit, wire_clk, wire_data, wire_out):
    not_data = circuit.new_wire()
    Not(circuit, wire_data, not_data)
    and_d_clk = circuit.new_wire()
    And(circuit, wire_data, wire_clk, and_d_clk)
    and_notd_clk = circuit.new_wire()
    And(circuit, not_data, wire_clk, and_notd_clk)
    neg_out = circuit.new_wire()
    Nor(circuit, and_notd_clk, neg_out, wire_out)
    Nor(circuit, and_d_clk, wire_out, neg_out)
    neg_out.assume(ONE)


def DFlipFlop(circuit, wire_clk, wire_data, wire_out):
    neg_clk = circuit.new_wire()
    Not(circuit, wire_clk, neg_clk)
    inter = circuit.new_wire()
    DLatch(circuit, wire_clk, wire_data, inter)
    DLatch(circuit, neg_clk, inter, wire_out)


class Reg8:
    def snapshot(self):
        val = 0
        for i in range(8):
            d = self.wires_out[i]
            if d == ONE:
                val += 2**i
            elif d == ZERO:
                pass
            else:
                return "X"
        return val

    def __init__(self, circuit, wire_clk, wires_data, wires_out):
        self.wires_out = wires_out
        for i in range(8):
            DFlipFlop(circuit, wire_clk, wires_data[i], wires_out[i])


class RAM:
    def snapshot(self):
        cells = []
        for i in range(256):
            cells.append(self.regs[i].snapshot())
        return cells

    def fill(self, data):
        for i in range(256):
            curr = data[i]
            for j in range(8):
                if curr % 2 == 0:
                    self.regs[i].latches[j].latch._data = ZERO
                else:
                    self.regs[i].latches[j].latch._data = ONE
                curr //= 2

    def __init__(
        self, circuit, wire_clk, wire_write, wires_addr, wires_data, wires_out
    ):
        self.regs = []
        self.sel_gates = []
        regs_outs = [list() for _ in range(8)]
        for byte in range(256):
            wires = []
            cell_addr = []
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
            self.sel_gates.append(Equals8(circuit, wires_addr, cell_addr, is_sel))
            self.sel_gates.append(And(circuit, is_sel, wire_write, is_wr))
            self.sel_gates.append(And(circuit, is_wr, wire_clk, is_wr_clk))
            self.regs.append(Reg8(circuit, is_wr_clk, wires_data, wires))

        self.muxes = []
        for i in range(8):
            self.muxes.append(Mux8x256(circuit, wires_addr, regs_outs[i], wires_out[i]))

    def update(self):
        for sel in self.sel_gates:
            sel.update()
        for reg in self.regs:
            reg.update()
        for mux in self.muxes:
            mux.update()
