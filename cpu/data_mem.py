from gates import Or
from adder import Adder8
from memory import FastRAM
from mux import Mux1x2Byte


def DataMemory(circuit, in_clk, in_addr, in_is_inc, in_is_dec, out_data):
    one = [circuit.one()] + [circuit.zero()] * 7
    min_one = [circuit.one()] * 8

    is_wr = circuit.new_wire()
    Or(circuit, in_is_inc, in_is_dec, is_wr)

    data_inc = [circuit.new_wire() for _ in range(8)]
    data_dec = [circuit.new_wire() for _ in range(8)]
    Adder8(circuit, out_data, one, circuit.zero(), data_inc, circuit.new_wire())
    Adder8(circuit, out_data, min_one, circuit.zero(), data_dec, circuit.new_wire())
    data_next = [circuit.new_wire() for _ in range(8)]
    Mux1x2Byte(circuit, in_is_dec, data_inc, data_dec, data_next)

    return FastRAM(
        circuit, in_clk, is_wr, in_addr, data_next, out_data, [0 for _ in range(256)]
    )
