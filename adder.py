from wire import *
from gates import *
from circuit import Circuit


def HalfAdder(circuit, in_a, in_b, out_sum, out_carry):
    Xor(circuit, in_a, in_b, out_sum)
    And(circuit, in_a, in_b, out_carry)


def FullAdder(circuit, in_a, in_b, in_carry, out_sum, out_carry):
    sum_ab = circuit.new_wire()
    carry1 = circuit.new_wire()
    carry2 = circuit.new_wire()
    HalfAdder(circuit, in_a, in_b, sum_ab, carry1)
    HalfAdder(circuit, sum_ab, in_carry, out_sum, carry2)
    Or(circuit, carry1, carry2, out_carry)


def Adder8(circuit, in_a, in_b, in_carry, out_sum, out_carry):
    carries = [in_carry] + [circuit.new_wire() for _ in range(7)] + [out_carry]
    for i in range(8):
        FullAdder(
            circuit,
            in_a[i],
            in_b[i],
            carries[i],
            out_sum[i],
            carries[i + 1],
        )
