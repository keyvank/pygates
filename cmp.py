from wire import *
from gates import *


def Equals(circuit, wire_in_a, wire_in_b, wire_out):
    xor_out = circuit.new_wire()
    Xor(circuit, wire_in_a, wire_in_b, xor_out)
    Not(circuit, xor_out, wire_out)


def MultiEquals(circuit, wires_a, wires_b, wire_out):
    if len(wires_a) != len(wires_b):
        raise Exception("Expected equal num of wires!")

    count = len(wires_a)
    not_eq_outs = []
    for i in range(count):
        not_eq_out = circuit.new_wire()
        Xor(circuit, wires_a[i], wires_b[i], not_eq_out)
        not_eq_outs.append(not_eq_out)

    inter = circuit.new_wire()
    Or(circuit, not_eq_outs[0], not_eq_outs[1], inter)
    for i in range(2, count):
        next_inter = circuit.new_wire()
        Or(circuit, inter, not_eq_outs[i], next_inter)
        inter = next_inter
    Not(circuit, inter, wire_out)
