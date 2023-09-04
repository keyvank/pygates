from wire import *
from gates import *


class Decoder1x2:
    def __init__(self, wire_enabled, wires_select, wires_out):
        not_addr0_wire = Wire()

        self.not_addr0 = Not(wires_select[0], not_addr0_wire)
        self.and0 = And(wire_enabled, not_addr0_wire, wires_out[0])
        self.and1 = And(wire_enabled, wires_select[0], wires_out[1])

    def update(self):
        self.not_addr0.update()
        self.and0.update()
        self.and1.update()
