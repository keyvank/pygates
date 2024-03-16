from circuit import Circuit
from wire import Wire
from memory import FastRAM

from .decoder import Decoder
from .pc import PC
from .p import P
from .data import DataMemory
from .assembler import compile


class CPU:
    def snapshot(self):
        print("P:", self.p.snapshot())
        print("PC:", self.pc.snapshot())
        print("RAM:", self.ram.snapshot())

    def __init__(self, circuit: Circuit, wire_clk: Wire, code: str):
        pc_out = [circuit.new_wire() for _ in range(8)]
        p_out = [circuit.new_wire() for _ in range(8)]
        data_mem_out = [circuit.new_wire() for _ in range(8)]
        inst_mem_out = [circuit.new_wire() for _ in range(8)]

        is_fwd = circuit.new_wire()  # if inst_mem_out[0:3] == 000
        is_bwd = circuit.new_wire()  # if inst_mem_out[0:3] == 010
        is_inc = circuit.new_wire()  # if inst_mem_out[0:3] == 001
        is_dec = circuit.new_wire()  # if inst_mem_out[0:3] == 011
        is_jmp = circuit.new_wire()  # if inst_mem_out[0] == 1
        Decoder(circuit, inst_mem_out, is_fwd, is_bwd, is_inc, is_dec, is_jmp)

        # PC =
        #   if is_jmp: instruction[1:8]
        #   else: PC + 1
        self.pc = PC(circuit, wire_clk, is_jmp, data_mem_out, inst_mem_out[1:8], pc_out)

        # P =
        #   if is_fwd: P + 1
        #   if is_bwd: P - 1
        #   else: P
        self.p = P(circuit, wire_clk, is_fwd, is_bwd, p_out)

        # Data[P] =
        #   if is_inc: Data[P] + 1
        #   if is_dec: Data[P] - 1
        #   else: Data[P]
        self.ram = DataMemory(circuit, wire_clk, p_out, is_inc, is_dec, data_mem_out)

        # Inst = Program[PC]
        self.rom = FastRAM(
            circuit,
            wire_clk,
            circuit.zero(),
            pc_out,
            [circuit.zero()] * 8,
            inst_mem_out,
            compile(code),
        )
