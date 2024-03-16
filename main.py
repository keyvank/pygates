#!/usr/bin/python3

from wire import ZERO, ONE
from circuit import Circuit
from cpu import CPU


if __name__ == "__main__":
    circ = Circuit()
    clk = circ.new_wire()

    OSCILLATOR = "OSCILLATOR"

    clk.put(OSCILLATOR, ZERO)
    clk_val = False

    code = "+>+[[->+>+<<]>[-<+>]<<[->>+>+<<<]>>[-<<+>>]>[-<+>]<]"

    cpu = CPU(circ, clk, code)

    print("Num components:", circ.num_components())
    while True:
        circ.stabilize()
        cpu.snapshot()
        if clk_val:
            clk.put(OSCILLATOR, ONE)
        else:
            clk.put(OSCILLATOR, ZERO)
        clk_val = not clk_val
