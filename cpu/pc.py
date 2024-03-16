from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *
from circuit import *


def PC(circuit, wire_clk, is_jmp, data, wires_addr, pc_out):
    zero = [circuit.zero()] * 8
    one = [circuit.one()] + [circuit.zero()] * 7

    is_data_zero = circuit.new_wire()
    is_data_not_zero = circuit.new_wire()
    should_jump = circuit.new_wire()
    MultiEquals(circuit, data, zero, is_data_zero)
    Not(circuit, is_data_zero, is_data_not_zero)
    And(circuit, is_jmp, is_data_not_zero, should_jump)

    pc_inc = [circuit.new_wire() for _ in range(8)]
    pc_next = [circuit.new_wire() for _ in range(8)]
    Adder8(circuit, pc_out, one, circuit.zero(), pc_inc, circuit.new_wire())
    Mux1x2Byte(
        circuit,
        should_jump,
        pc_inc,
        wires_addr + [circuit.zero()],
        pc_next,
    )
    return Reg8(circuit, wire_clk, pc_next, pc_out, 0)
