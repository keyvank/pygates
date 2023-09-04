from wire import *
from gates import *


class Equals:
    def __init__(self, wire_in_a, wire_in_b, wire_out):
        xor_out = Wire()
        self.xor = Xor(wire_in_a, wire_in_b, xor_out)
        self.n = Not(xor_out, wire_out)

    def update(self):
        self.xor.update()
        self.n.update()


class Equals8:
    def __init__(self, wires_a, wires_b, wire_out):
        self.eqs = []
        eq_outs = []
        for i in range(8):
            eq_out = Wire()
            self.eqs.append(Equals(wires_a[i], wires_b[i], eq_out))
            eq_outs.append(eq_out)

        inter = Wire()
        self.ands = [And(eq_outs[0], eq_outs[1], inter)]
        for i in range(2, 7):
            next_inter = Wire()
            self.ands.append(And(inter, eq_outs[i], next_inter))
            inter = next_inter
        self.ands.append(And(inter, eq_outs[7], wire_out))

    def update(self):
        for eq in self.eqs:
            eq.update()
        for a in self.ands:
            a.update()


class Equals3:
    def __init__(self, wires_a, wires_b, wire_out):
        self.eqs = []
        eq_outs = []
        for i in range(3):
            eq_out = Wire()
            self.eqs.append(Equals(wires_a[i], wires_b[i], eq_out))
            eq_outs.append(eq_out)

        inter = Wire()
        self.and1 = And(eq_outs[0], eq_outs[1], inter)
        self.and2 = And(inter, eq_outs[2], wire_out)

    def update(self):
        for eq in self.eqs:
            eq.update()
        self.and1.update()
        self.and2.update()
