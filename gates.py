from wire import *
from transistor import *


def Not(circuit, wire_in, wire_out):
    circuit.add_component(PTransistor(circuit, wire_in, circuit.one(), wire_out))
    circuit.add_component(NTransistor(circuit, wire_in, circuit.zero(), wire_out))


def Nand(circuit, wire_a, wire_b, wire_out):
    inter = circuit.new_wire()
    circuit.add_component(PTransistor(circuit, wire_a, circuit.one(), wire_out))
    circuit.add_component(PTransistor(circuit, wire_b, circuit.one(), wire_out))
    circuit.add_component(NTransistor(circuit, wire_a, circuit.zero(), inter))
    circuit.add_component(NTransistor(circuit, wire_b, inter, wire_out))


def And(circuit, wire_in_a, wire_in_b, wire_out):
    not_out = circuit.new_wire()
    Nand(circuit, wire_in_a, wire_in_b, not_out)
    Not(circuit, not_out, wire_out)


def Or(circuit, wire_in_a, wire_in_b, wire_out):
    not_out = circuit.new_wire()
    Nor(circuit, wire_in_a, wire_in_b, not_out)
    Not(circuit, not_out, wire_out)


def Nor(circuit, wire_a, wire_b, wire_out):
    inter = circuit.new_wire()
    circuit.add_component(PTransistor(circuit, wire_a, circuit.one(), inter))
    circuit.add_component(PTransistor(circuit, wire_b, inter, wire_out))
    circuit.add_component(NTransistor(circuit, wire_a, circuit.zero(), wire_out))
    circuit.add_component(NTransistor(circuit, wire_b, circuit.zero(), wire_out))


def Xor(circuit, wire_a, wire_b, wire_out):
    a_not = circuit.new_wire()
    b_not = circuit.new_wire()
    Not(circuit, wire_a, a_not)
    Not(circuit, wire_b, b_not)

    inter1 = circuit.new_wire()
    circuit.add_component(PTransistor(circuit, b_not, circuit.one(), inter1))
    circuit.add_component(PTransistor(circuit, wire_a, inter1, wire_out))
    inter2 = circuit.new_wire()
    circuit.add_component(PTransistor(circuit, wire_b, circuit.one(), inter2))
    circuit.add_component(PTransistor(circuit, a_not, inter2, wire_out))

    inter3 = circuit.new_wire()
    circuit.add_component(NTransistor(circuit, wire_b, circuit.zero(), inter3))
    circuit.add_component(NTransistor(circuit, wire_a, inter3, wire_out))
    inter4 = circuit.new_wire()
    circuit.add_component(NTransistor(circuit, b_not, circuit.zero(), inter4))
    circuit.add_component(NTransistor(circuit, a_not, inter4, wire_out))
