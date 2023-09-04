from wire import *
from transistor import *


class Not:
    def __init__(self, wire_in, wire_out):
        self.p = PTransistor(wire_in, Wire.one(), wire_out)
        self.n = NTransistor(wire_in, Wire.zero(), wire_out)

    def update(self):
        self.p.update()
        self.n.update()


class Nand:
    def __init__(self, wire_a, wire_b, wire_out):
        inter = Wire()

        self.p1 = PTransistor(wire_a, Wire.one(), wire_out)
        self.p2 = PTransistor(wire_b, Wire.one(), wire_out)
        self.n1 = NTransistor(wire_a, Wire.zero(), inter)
        self.n2 = NTransistor(wire_b, inter, wire_out)

    def update(self):
        self.n1.update()
        self.n2.update()
        self.p1.update()
        self.p2.update()


class And:
    def __init__(self, wire_in_a, wire_in_b, wire_out):
        not_out = Wire()

        self.nand = Nand(wire_in_a, wire_in_b, not_out)
        self.n = Not(not_out, wire_out)

    def update(self):
        self.nand.update()
        self.n.update()


class Or:
    def __init__(self, wire_in_a, wire_in_b, wire_out):
        not_a = Wire()
        not_b = Wire()

        self.gate_not_a = Not(wire_in_a, not_a)
        self.gate_not_b = Not(wire_in_b, not_b)
        self.nand = Nand(not_a, not_b, wire_out)

    def update(self):
        self.gate_not_a.update()
        self.gate_not_b.update()
        self.nand.update()


class Xor:
    def __init__(self, wire_in_a, wire_in_b, wire_out):
        wire_not_a = Wire()
        wire_not_b = Wire()
        wire_a_and_not_b = Wire()
        wire_b_and_not_a = Wire()

        self.gate_not_a = Not(wire_in_a, wire_not_a)
        self.gate_not_b = Not(wire_in_b, wire_not_b)
        self.gate_a_and_not_b = And(wire_in_a, wire_not_b, wire_a_and_not_b)
        self.gate_b_and_not_a = And(wire_in_b, wire_not_a, wire_b_and_not_a)
        self.gate_or = Or(wire_a_and_not_b, wire_b_and_not_a, wire_out)

    def update(self):
        self.gate_not_a.update()
        self.gate_not_b.update()
        self.gate_a_and_not_b.update()
        self.gate_b_and_not_a.update()
        self.gate_or.update()
