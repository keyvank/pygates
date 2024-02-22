from wire import *
from gates import *


def Mux1x2(circuit, wire_select, wires_data, wire_out):
    wire_select_not = circuit.new_wire()
    and1_out = circuit.new_wire()
    and2_out = circuit.new_wire()
    Not(circuit, wire_select[0], wire_select_not)
    And(circuit, wire_select_not, wires_data[0], and1_out)
    And(circuit, wire_select[0], wires_data[1], and2_out)
    Or(circuit, and1_out, and2_out, wire_out)


def Mux(bits, sub_mux):
    def f(circuit, wires_select, wires_data, wire_out):
        out_mux1 = circuit.new_wire()
        out_mux2 = circuit.new_wire()

        sub_mux(
            circuit,
            wires_select[0 : bits - 1],
            wires_data[0 : 2 ** (bits - 1)],
            out_mux1,
        )
        sub_mux(
            circuit,
            wires_select[0 : bits - 1],
            wires_data[2 ** (bits - 1) : 2**bits],
            out_mux2,
        )
        Mux1x2(
            circuit, [wires_select[bits - 1]], [out_mux1, out_mux2], wire_out
        )

    return f


Mux2x4 = Mux(2, Mux1x2)
Mux3x8 = Mux(3, Mux2x4)
Mux4x16 = Mux(4, Mux3x8)
Mux5x32 = Mux(5, Mux4x16)
Mux6x64 = Mux(6, Mux5x32)
Mux7x128 = Mux(7, Mux6x64)
Mux8x256 = Mux(8, Mux7x128)
