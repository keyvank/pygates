from wire import *
from gates import *
from circuit import Circuit


class HalfAdder:
    def __init__(self, circuit, wire_a, wire_b, wire_out, wire_carry_out):
        self.gate_sum = Xor(circuit, wire_a, wire_b, wire_out)
        self.gate_carry = And(circuit, wire_a, wire_b, wire_carry_out)

    def update(self):
        self.gate_sum.update()
        self.gate_carry.update()


class FullAdder:
    def __init__(
        self, circuit, wire_a, wire_b, wire_carry_in, wire_out, wire_carry_out
    ):
        wire_ab = circuit.new_wire()
        wire_c1 = circuit.new_wire()
        wire_c2 = circuit.new_wire()

        self.ha_1 = HalfAdder(circuit, wire_a, wire_b, wire_ab, wire_c1)
        self.ha_2 = HalfAdder(circuit, wire_ab, wire_carry_in, wire_out, wire_c2)
        self.carry = Or(circuit, wire_c1, wire_c2, wire_carry_out)

    def update(self):
        self.ha_1.update()
        self.ha_2.update()
        self.carry.update()


class Adder8:
    def __init__(
        self, circuit, wires_a, wires_b, wire_carry_in, wires_out, wire_carry_out
    ):
        carries = [wire_carry_in] + [Wire() for _ in range(7)] + [wire_carry_out]

        self.adders = [
            FullAdder(
                circuit,
                wires_a[i],
                wires_b[i],
                carries[i],
                wires_out[i],
                carries[i + 1],
            )
            for i in range(8)
        ]

    def update(self):
        for adder in self.adders:
            adder.update()
