from circuit import Circuit
from wire import Wire
from memory import FastRAM

from .decoder import Decoder
from .pc import PC
from .p import P
from .data_mem import DataMemory
from .inst_mem import InstructionMemory


class CPU:
    def snapshot(self):
        print("P:", self.p.snapshot())
        print("PC:", self.pc.snapshot())
        print("RAM:", self.ram.snapshot())

    def __init__(self, circuit: Circuit, wire_clk: Wire, code: str):
        inst_pointer = [circuit.new_wire() for _ in range(8)]
        inst = [circuit.new_wire() for _ in range(8)]

        data_pointer = [circuit.new_wire() for _ in range(8)]
        data = [circuit.new_wire() for _ in range(8)]

        # inst = Inst[inst_pointer]
        self.rom = InstructionMemory(circuit, wire_clk, inst_pointer, inst, code)

        is_fwd = circuit.new_wire()  # if inst[0:3] == 000
        is_bwd = circuit.new_wire()  # if inst[0:3] == 010
        is_inc = circuit.new_wire()  # if inst[0:3] == 001
        is_dec = circuit.new_wire()  # if inst[0:3] == 011
        is_jmp = circuit.new_wire()  # if inst[0] == 1
        Decoder(circuit, inst, is_fwd, is_bwd, is_inc, is_dec, is_jmp)

        # inst_pointer =
        #   if is_jmp: inst[1:8]
        #   else: inst_pointer + 1
        self.pc = PC(circuit, wire_clk, is_jmp, data, inst[1:8], inst_pointer)

        # data_pointer =
        #   if is_fwd: data_pointer + 1
        #   if is_bwd: data_pointer - 1
        #   else: P
        self.p = P(circuit, wire_clk, is_fwd, is_bwd, data_pointer)

        # data = Data[data_pointer]
        #   if is_inc: Data[data_pointer] + 1
        #   if is_dec: Data[data_pointer] - 1
        #   else: Data[data_pointer]
        self.ram = DataMemory(circuit, wire_clk, data_pointer, is_inc, is_dec, data)
