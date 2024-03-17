from wire import *
from transistor import *


def Not(circuit, inp, out):
    circuit.add_component(PTransistor(inp, circuit.one(), out))
    circuit.add_component(NTransistor(inp, circuit.zero(), out))


def Nand(circuit, in_a, in_b, out):
    inter = circuit.new_wire()
    circuit.add_component(PTransistor(in_a, circuit.one(), out))
    circuit.add_component(PTransistor(in_b, circuit.one(), out))
    circuit.add_component(NTransistor(in_a, circuit.zero(), inter))
    circuit.add_component(NTransistor(in_b, inter, out))


def And(circuit, in_a, in_b, out):
    not_out = circuit.new_wire()
    Nand(circuit, in_a, in_b, not_out)
    Not(circuit, not_out, out)


def Or(circuit, in_a, in_b, out):
    not_out = circuit.new_wire()
    Nor(circuit, in_a, in_b, not_out)
    Not(circuit, not_out, out)


def Nor(circuit, in_a, in_b, out):
    inter = circuit.new_wire()
    circuit.add_component(PTransistor(in_a, circuit.one(), inter))
    circuit.add_component(PTransistor(in_b, inter, out))
    circuit.add_component(NTransistor(in_a, circuit.zero(), out))
    circuit.add_component(NTransistor(in_b, circuit.zero(), out))


def Xor(circuit, in_a, in_b, out):
    a_not = circuit.new_wire()
    b_not = circuit.new_wire()
    Not(circuit, in_a, a_not)
    Not(circuit, in_b, b_not)

    inter1 = circuit.new_wire()
    circuit.add_component(PTransistor(b_not, circuit.one(), inter1))
    circuit.add_component(PTransistor(in_a, inter1, out))
    inter2 = circuit.new_wire()
    circuit.add_component(PTransistor(in_b, circuit.one(), inter2))
    circuit.add_component(PTransistor(a_not, inter2, out))

    inter3 = circuit.new_wire()
    circuit.add_component(NTransistor(in_b, circuit.zero(), inter3))
    circuit.add_component(NTransistor(in_a, inter3, out))
    inter4 = circuit.new_wire()
    circuit.add_component(NTransistor(b_not, circuit.zero(), inter4))
    circuit.add_component(NTransistor(a_not, inter4, out))


def Forward(circuit, inp, out):
    tmp = circuit.new_wire()
    Not(circuit, inp, tmp)
    Not(circuit, tmp, out)
