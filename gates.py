from wire import *
from transistor import *


class Not:
    def __init__(self, circuit, wire_in, wire_out):
        self.p = PTransistor(circuit, wire_in, circuit.one(), wire_out)
        self.n = NTransistor(circuit, wire_in, circuit.zero(), wire_out)

    def update(self):
        self.p.update()
        self.n.update()


class Nand:
    def __init__(self, circuit, wire_a, wire_b, wire_out):
        inter = circuit.new_wire()

        self.p1 = PTransistor(circuit, wire_a, circuit.one(), wire_out)
        self.p2 = PTransistor(circuit, wire_b, circuit.one(), wire_out)
        self.n1 = NTransistor(circuit, wire_a, circuit.zero(), inter)
        self.n2 = NTransistor(circuit, wire_b, inter, wire_out)

    def update(self):
        self.n1.update()
        self.n2.update()
        self.p1.update()
        self.p2.update()


class And:
    def __init__(self, circuit, wire_in_a, wire_in_b, wire_out):
        not_out = circuit.new_wire()

        self.nand = Nand(circuit, wire_in_a, wire_in_b, not_out)
        self.n = Not(circuit, not_out, wire_out)

    def update(self):
        self.nand.update()
        self.n.update()


class Or:
    def __init__(self, circuit, wire_in_a, wire_in_b, wire_out):
        not_a = circuit.new_wire()
        not_b = circuit.new_wire()

        self.gate_not_a = Not(circuit, wire_in_a, not_a)
        self.gate_not_b = Not(circuit, wire_in_b, not_b)
        self.nand = Nand(circuit, not_a, not_b, wire_out)

    def update(self):
        self.gate_not_a.update()
        self.gate_not_b.update()
        self.nand.update()


class Xor:
    def __init__(self, circuit, wire_in_a, wire_in_b, wire_out):
        wire_not_a = circuit.new_wire()
        wire_not_b = circuit.new_wire()
        wire_a_and_not_b = circuit.new_wire()
        wire_b_and_not_a = circuit.new_wire()

        self.gate_not_a = Not(circuit, wire_in_a, wire_not_a)
        self.gate_not_b = Not(circuit, wire_in_b, wire_not_b)
        self.gate_a_and_not_b = And(circuit, wire_in_a, wire_not_b, wire_a_and_not_b)
        self.gate_b_and_not_a = And(circuit, wire_in_b, wire_not_a, wire_b_and_not_a)
        self.gate_or = Or(circuit, wire_a_and_not_b, wire_b_and_not_a, wire_out)

    def update(self):
        self.gate_not_a.update()
        self.gate_not_b.update()
        self.gate_a_and_not_b.update()
        self.gate_b_and_not_a.update()
        self.gate_or.update()
