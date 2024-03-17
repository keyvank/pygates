from wire import *
from gates import *


def Equals(circuit, in_a, in_b, out_eq):
    xor_out = circuit.new_wire()
    Xor(circuit, in_a, in_b, xor_out)
    Not(circuit, xor_out, out_eq)


def MultiEquals(circuit, in_a, in_b, out_eq):
    if len(in_a) != len(in_b):
        raise Exception("Expected equal num of wires!")

    count = len(in_a)
    xor_outs = []
    for i in range(count):
        xor_out = circuit.new_wire()
        Xor(circuit, in_a[i], in_b[i], xor_out)
        xor_outs.append(xor_out)

    inter = circuit.new_wire()
    Or(circuit, xor_outs[0], xor_outs[1], inter)
    for i in range(2, count):
        next_inter = circuit.new_wire()
        Or(circuit, inter, xor_outs[i], next_inter)
        inter = next_inter
    Not(circuit, inter, out_eq)
