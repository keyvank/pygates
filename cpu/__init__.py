from circuit import Circuit
from wire import Wire
from gates import Forward

from .decoder import Decoder
from .data_pnt import DataPointer
from .data_mem import DataMemory
from .inst_pnt import InstructionPointer
from .inst_mem import InstructionMemory


class CPU:
    def snapshot(self):
        print("Data Pointer:", self.data_pointer.snapshot())
        print("Instruction Pointer:", self.inst_pointer.snapshot())
        print("RAM:", self.ram.snapshot())

    def __init__(
        self,
        circuit: Circuit,
        in_clk: Wire,
        code: str,
        out_ready: Wire,
        out_data,
    ):
        inst_pointer = [circuit.new_wire() for _ in range(8)]
        inst = [circuit.new_wire() for _ in range(8)]

        data_pointer = [circuit.new_wire() for _ in range(8)]
        data = [circuit.new_wire() for _ in range(8)]

        is_fwd = circuit.new_wire()
        is_bwd = circuit.new_wire()
        is_inc = circuit.new_wire()
        is_dec = circuit.new_wire()
        is_jmp = circuit.new_wire()
        is_prnt = circuit.new_wire()

        Forward(circuit, is_prnt, out_ready)
        for i in range(8):
            Forward(circuit, data[i], out_data[i])

        # inst = Inst[inst_pointer]
        self.rom = InstructionMemory(circuit, in_clk, inst_pointer, inst, code)

        # is_fwd = inst[0:4] == 0000
        # is_bwd = inst[0:4] == 0100
        # is_inc = inst[0:4] == 0010
        # is_dec = inst[0:4] == 0110
        # is_prnt = inst[0:4] == 0001
        # is_jmp = inst[0] == 1
        Decoder(circuit, inst, is_fwd, is_bwd, is_inc, is_dec, is_jmp, is_prnt)

        # inst_pointer =
        #   if is_jmp: inst[1:8]
        #   else: inst_pointer + 1
        self.inst_pointer = InstructionPointer(
            circuit, in_clk, is_jmp, data, inst[1:8], inst_pointer
        )

        # data_pointer =
        #   if is_fwd: data_pointer + 1
        #   if is_bwd: data_pointer - 1
        #   else: P
        self.data_pointer = DataPointer(circuit, in_clk, is_fwd, is_bwd, data_pointer)

        # data = Data[data_pointer]
        #   if is_inc: Data[data_pointer] + 1
        #   if is_dec: Data[data_pointer] - 1
        #   else: Data[data_pointer]
        self.ram = DataMemory(circuit, in_clk, data_pointer, is_inc, is_dec, data)
