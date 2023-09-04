from wire import *
from mux import *


class DLatch:
    def __init__(self, wire_enabled, wire_data, wire_out):
        self.wire_enabled = wire_enabled
        self.wire_data = wire_data
        self.wire_out = wire_out
        self._data = ZERO

    def update(self):
        en = self.wire_enabled.get()
        if en == ONE:
            self._data = self.wire_data.get()
        self.wire_out.put(self, self._data)


class Reg8:
    def __init__(self, wire_enabled, wires_data, wires_out):
        self.latches = [
            DLatch(wire_enabled, wires_data[i], wires_out[i]) for i in range(8)
        ]

    def update(self):
        for latch in self.latches:
            latch.update()


class RAM:
    def fill(self, data):
        for i in range(256):
            curr = data[i]
            for j in range(8):
                if curr % 2 == 0:
                    self.regs[i].latches[j]._data = ZERO
                else:
                    self.regs[i].latches[j]._data = ONE
                curr //= 2

    def __init__(self, wire_write, wires_addr, wires_data, wires_out):
        self.regs = []
        regs_outs = [list() for _ in range(8)]
        for byte in range(256):
            wires = []
            for bit in range(8):
                w = Wire()
                wires.append(w)
                regs_outs[bit].append(w)
            self.regs.append(Reg8(Wire.zero(), wires_data, wires))

        self.muxes = []
        for i in range(8):
            self.muxes.append(Mux8x256(wires_addr, regs_outs[i], wires_out[i]))

    def update(self):
        for reg in self.regs:
            reg.update()
        for mux in self.muxes:
            mux.update()
