#!/usr/bin/python3

from wire import BATTERY, ZERO, ONE
from circuit import Circuit
from cpu import CPU


if __name__ == "__main__":
    circ = Circuit()
    clk = circ.new_wire()
    clk.put(BATTERY, ZERO)
    clk_val = False

    code = "+>+[[->+>+<<]>[-<+>]<<[->>+>+<<<]>>[-<<+>>]>[-<+>]<]"

    cpu = CPU(circ, clk, code)
    print(circ._transistors.__len__())
    while True:
        circ.stabilize()
        cpu.snapshot()
        if clk_val:
            clk.put(BATTERY, ONE)
        else:
            clk.put(BATTERY, ZERO)
        clk_val = not clk_val
