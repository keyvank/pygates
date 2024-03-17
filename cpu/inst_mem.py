from memory import FastRAM
from .assembler import compile


def InstructionMemory(circuit, in_clk, in_inst_pointer, out_inst, code=""):
    return FastRAM(
        circuit,
        in_clk,
        circuit.zero(),
        in_inst_pointer,
        [circuit.zero()] * 8,
        out_inst,
        compile(code),
    )
