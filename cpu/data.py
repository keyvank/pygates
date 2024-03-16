from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *
from circuit import *


def DataMemory(circuit, wire_clk, addr, is_inc, is_dec, data_out):
    one = [circuit.one()] + [circuit.zero()] * 7
    min_one = [circuit.one()] * 8

    is_wr = circuit.new_wire()
    Or(circuit, is_inc, is_dec, is_wr)

    data_inc = [circuit.new_wire() for _ in range(8)]
    data_dec = [circuit.new_wire() for _ in range(8)]
    Adder8(circuit, data_out, one, circuit.zero(), data_inc, circuit.new_wire())
    Adder8(circuit, data_out, min_one, circuit.zero(), data_dec, circuit.new_wire())
    data_next = [circuit.new_wire() for _ in range(8)]
    Mux1x2Byte(circuit, is_dec, data_inc, data_dec, data_next)

    return FastRAM(
        circuit, wire_clk, is_wr, addr, data_next, data_out, [0 for _ in range(256)]
    )
