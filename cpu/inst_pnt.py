from gates import And, Not
from mux import Mux1x2Byte
from adder import Adder8
from cmp import MultiEquals
from memory import Reg8


def InstructionPointer(circuit, wire_clk, is_jmp, data, wires_addr, inst_pointer):
    zero = [circuit.zero()] * 8
    one = [circuit.one()] + [circuit.zero()] * 7

    # should_jump = Data[DataPointer] != 0 && is_jmp
    is_data_zero = circuit.new_wire()
    is_data_not_zero = circuit.new_wire()
    should_jump = circuit.new_wire()
    MultiEquals(circuit, data, zero, is_data_zero)
    Not(circuit, is_data_zero, is_data_not_zero)
    And(circuit, is_jmp, is_data_not_zero, should_jump)

    # InstPointer = should_jump ? wires_addr : InstPointer + 1
    inst_pointer_inc = [circuit.new_wire() for _ in range(8)]
    inst_pointer_next = [circuit.new_wire() for _ in range(8)]
    Adder8(
        circuit, inst_pointer, one, circuit.zero(), inst_pointer_inc, circuit.new_wire()
    )
    Mux1x2Byte(
        circuit,
        should_jump,
        inst_pointer_inc,
        wires_addr + [circuit.zero()],
        inst_pointer_next,
    )

    return Reg8(circuit, wire_clk, inst_pointer_next, inst_pointer, 0)
