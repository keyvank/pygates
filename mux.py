from wire import *
from gates import *


class Mux1x2:
    def __init__(self, circuit, wire_select, wires_data, wire_out):
        wire_select_not = circuit.new_wire()
        and1_out = circuit.new_wire()
        and2_out = circuit.new_wire()

        self.sel_not_gate = Not(circuit, wire_select[0], wire_select_not)
        self.and1_gate = And(circuit, wire_select_not, wires_data[0], and1_out)
        self.and2_gate = And(circuit, wire_select[0], wires_data[1], and2_out)
        self.or_gate = Or(circuit, and1_out, and2_out, wire_out)

    def update(self):
        self.sel_not_gate.update()
        self.and1_gate.update()
        self.and2_gate.update()
        self.or_gate.update()


def Mux(name, bits, sub_mux):
    def __init__(self, circuit, wires_select, wires_data, wire_out):
        out_mux1 = circuit.new_wire()
        out_mux2 = circuit.new_wire()

        self.mux1 = sub_mux(
            circuit,
            wires_select[0 : bits - 1],
            wires_data[0 : 2 ** (bits - 1)],
            out_mux1,
        )
        self.mux2 = sub_mux(
            circuit,
            wires_select[0 : bits - 1],
            wires_data[2 ** (bits - 1) : 2**bits],
            out_mux2,
        )
        self.mux = Mux1x2(
            circuit, [wires_select[bits - 1]], [out_mux1, out_mux2], wire_out
        )

    def update(self):
        self.mux1.update()
        self.mux2.update()
        self.mux.update()

    return type(name, (object,), {"__init__": __init__, "update": update})


Mux2x4 = Mux("Mux2x4", 2, Mux1x2)
Mux3x8 = Mux("Mux3x8", 3, Mux2x4)
Mux4x16 = Mux("Mux4x16", 4, Mux3x8)
Mux5x32 = Mux("Mux5x32", 5, Mux4x16)
Mux6x64 = Mux("Mux6x64", 6, Mux5x32)
Mux7x128 = Mux("Mux7x128", 7, Mux6x64)
Mux8x256 = Mux("Mux8x256", 8, Mux7x128)
