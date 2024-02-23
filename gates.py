from wire import *
from transistor import *


def Not(circuit, wire_in, wire_out):
    circuit.new_transistor(PTransistor(circuit, wire_in, circuit.one(), wire_out))
    circuit.new_transistor(NTransistor(circuit, wire_in, circuit.zero(), wire_out))


def Nand(circuit, wire_a, wire_b, wire_out):
    inter = circuit.new_wire()
    circuit.new_transistor(PTransistor(circuit, wire_a, circuit.one(), wire_out))
    circuit.new_transistor(PTransistor(circuit, wire_b, circuit.one(), wire_out))
    circuit.new_transistor(NTransistor(circuit, wire_a, circuit.zero(), inter))
    circuit.new_transistor(NTransistor(circuit, wire_b, inter, wire_out))


def And(circuit, wire_in_a, wire_in_b, wire_out):
    not_out = circuit.new_wire()
    Nand(circuit, wire_in_a, wire_in_b, not_out)
    Not(circuit, not_out, wire_out)


def Or(circuit, wire_in_a, wire_in_b, wire_out):
    not_a = circuit.new_wire()
    not_b = circuit.new_wire()
    Not(circuit, wire_in_a, not_a)
    Not(circuit, wire_in_b, not_b)
    Nand(circuit, not_a, not_b, wire_out)


def Nor(circuit, wire_in_a, wire_in_b, wire_out):
    or_ab = circuit.new_wire()
    Or(circuit, wire_in_a, wire_in_b, or_ab)
    Not(circuit, or_ab, wire_out)


def Xor(circuit, wire_in_a, wire_in_b, wire_out):
    wire_not_a = circuit.new_wire()
    wire_not_b = circuit.new_wire()
    wire_a_and_not_b = circuit.new_wire()
    wire_b_and_not_a = circuit.new_wire()
    Not(circuit, wire_in_a, wire_not_a)
    Not(circuit, wire_in_b, wire_not_b)
    And(circuit, wire_in_a, wire_not_b, wire_a_and_not_b)
    And(circuit, wire_in_b, wire_not_a, wire_b_and_not_a)
    Or(circuit, wire_a_and_not_b, wire_b_and_not_a, wire_out)
