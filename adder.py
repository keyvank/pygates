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
        carries = (
            [wire_carry_in] + [circuit.new_wire() for _ in range(7)] + [wire_carry_out]
        )

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


def num_to_wires(num):
    wires = []
    for i in range(8):
        bit = (num >> i) & 1
        wires.append(Wire.one() if bit else Wire.zero())
    return wires


def wires_to_num(wires):
    out = 0
    for i, w in enumerate(wires):
        if w.get() == ONE:
            out += 2**i
    return out


if __name__ == "__main__":
    circuit = Circuit()
    for x in range(256):
        for y in range(256):
            wires_x = num_to_wires(x)
            wires_y = num_to_wires(y)
            wires_out = [Wire() for _ in range(8)]
            adder = Adder8(
                circuit, wires_x, wires_y, Wire.zero(), wires_out, Wire.zero()
            )
            adder.update()
            out = wires_to_num(wires_out)
            if out != (x + y) % 256:
                print("Adder is not working!")
