from wire import *
from transistor import *
from gates import *
from mux import *
from adder import *
from cmp import *
from memory import *
from circuit import *


def P(circuit, wire_clk, is_fwd, is_bwd, p_out):
    one = [circuit.one()] + [circuit.zero()] * 7
    min_one = [circuit.one()] * 8

    p_next = [circuit.new_wire() for _ in range(8)]
    is_fwd_bwd = circuit.new_wire()
    p_inter = [circuit.new_wire() for _ in range(8)]
    p_inc = [circuit.new_wire() for _ in range(8)]
    p_dec = [circuit.new_wire() for _ in range(8)]
    Adder8(circuit, p_out, one, circuit.zero(), p_inc, circuit.new_wire())
    Adder8(circuit, p_out, min_one, circuit.zero(), p_dec, circuit.new_wire())
    Or(circuit, is_fwd, is_bwd, is_fwd_bwd)
    Mux1x2Byte(circuit, is_bwd, p_inc, p_dec, p_inter)
    Mux1x2Byte(circuit, is_fwd_bwd, p_out, p_inter, p_next)
    return Reg8(circuit, wire_clk, p_next, p_out, 0)
