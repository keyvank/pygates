from memory import RAM
from .assembler import compile


def InstructionMemory(circuit, wire_clk, inst_pointer, inst, code):
    return RAM(
        circuit,
        wire_clk,
        circuit.zero(),
        inst_pointer,
        [circuit.zero()] * 8,
        inst,
        compile(code),
    )
