class CPU:
    def snapshot(self):
        print("PC:", self.pc.snapshot())
        print("PC INC:", [w.get() for w in self.pc_inc])

    def __init__(self, circuit, wire_clk, wires_out):
        one = [circuit.one()] + [circuit.zero()] * 7
        pc_out = [circuit.new_wire() for _ in range(8)]
        self.pc_inc = [circuit.new_wire() for _ in range(8)]
        Adder8(circuit, pc_out, one, circuit.zero(), self.pc_inc, circuit.new_wire())
        self.pc = Reg8(circuit, wire_clk, self.pc_inc, pc_out, 0)
