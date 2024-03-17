from gates import And, Not
from mux import Mux1x2Byte
from adder import Adder8
from cmp import MultiEquals
from memory import Reg8


def InstructionPointer(circuit, in_clk, in_is_jnz, in_data, in_addr, out_inst_pointer):
    zero = [circuit.zero()] * 8
    one = [circuit.one()] + [circuit.zero()] * 7

    # should_jump = Data[DataPointer] != 0 && in_is_jnz
    is_data_zero = circuit.new_wire()
    is_data_not_zero = circuit.new_wire()
    should_jump = circuit.new_wire()
    MultiEquals(circuit, in_data, zero, is_data_zero)
    Not(circuit, is_data_zero, is_data_not_zero)
    And(circuit, in_is_jnz, is_data_not_zero, should_jump)

    # InstPointer = should_jump ? in_addr : InstPointer + 1
    inst_pointer_inc = [circuit.new_wire() for _ in range(8)]
    inst_pointer_next = [circuit.new_wire() for _ in range(8)]
    Adder8(
        circuit,
        out_inst_pointer,
        one,
        circuit.zero(),
        inst_pointer_inc,
        circuit.new_wire(),
    )
    Mux1x2Byte(
        circuit,
        should_jump,
        inst_pointer_inc,
        in_addr + [circuit.zero()],
        inst_pointer_next,
    )

    return Reg8(circuit, in_clk, inst_pointer_next, out_inst_pointer, 0)
