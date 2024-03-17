from gates import Or
from mux import Mux1x2Byte
from adder import Adder8
from memory import Reg8


def DataPointer(circuit, wire_clk, is_fwd, is_bwd, data_pointer):
    one = [circuit.one()] + [circuit.zero()] * 7
    minus_one = [circuit.one()] * 8

    # data_pointer_inc = data_pointer + 1
    data_pointer_inc = [circuit.new_wire() for _ in range(8)]
    Adder8(
        circuit, data_pointer, one, circuit.zero(), data_pointer_inc, circuit.new_wire()
    )

    # data_pointer_inc = data_pointer - 1
    data_pointer_dec = [circuit.new_wire() for _ in range(8)]
    Adder8(
        circuit,
        data_pointer,
        minus_one,
        circuit.zero(),
        data_pointer_dec,
        circuit.new_wire(),
    )

    data_pointer_next = [circuit.new_wire() for _ in range(8)]
    is_fwd_bwd = circuit.new_wire()
    Or(circuit, is_fwd, is_bwd, is_fwd_bwd)
    tmp = [circuit.new_wire() for _ in range(8)]
    Mux1x2Byte(circuit, is_bwd, data_pointer_inc, data_pointer_dec, tmp)
    Mux1x2Byte(circuit, is_fwd_bwd, data_pointer, tmp, data_pointer_next)

    return Reg8(circuit, wire_clk, data_pointer_next, data_pointer, 0)
