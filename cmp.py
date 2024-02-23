from wire import *
from gates import *


def Equals(circuit, wire_in_a, wire_in_b, wire_out):
    xor_out = circuit.new_wire()
    Xor(circuit, wire_in_a, wire_in_b, xor_out)
    Not(circuit, xor_out, wire_out)


def Equals8(circuit, wires_a, wires_b, wire_out):
    not_eq_outs = []
    for i in range(8):
        not_eq_out = circuit.new_wire()
        Xor(circuit, wires_a[i], wires_b[i], not_eq_out)
        not_eq_outs.append(not_eq_out)

    inter = circuit.new_wire()
    Or(circuit, not_eq_outs[0], not_eq_outs[1], inter)
    for i in range(2, 7):
        next_inter = circuit.new_wire()
        Or(circuit, inter, not_eq_outs[i], next_inter)
        inter = next_inter
    not_res = circuit.new_wire()
    Or(circuit, inter, not_eq_outs[7], not_res)
    Not(circuit, not_res, wire_out)


def Equals3(circuit, wires_a, wires_b, wire_out):
    eq_outs = []
    for i in range(3):
        eq_out = circuit.new_wire()
        Equals(circuit, wires_a[i], wires_b[i], eq_out)
        eq_outs.append(eq_out)

    inter = circuit.new_wire()
    And(circuit, eq_outs[0], eq_outs[1], inter)
    And(circuit, inter, eq_outs[2], wire_out)
