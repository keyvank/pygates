#!/usr/bin/python3

from wire import ZERO, ONE
from circuit import Circuit
from cpu import CPU
from utils import wires_to_num


if __name__ == "__main__":
    circ = Circuit()
    clk = circ.new_wire()

    out_ready = circ.new_wire()
    out = [circ.new_wire() for _ in range(8)]

    OSCILLATOR = "OSCILLATOR"

    clk.put(OSCILLATOR, ZERO)

    code = "+>+[.[->+>+<<]>[-<+>]<<[->>+>+<<<]>>[-<<+>>]>[-<+>]<]"

    cpu = CPU(circ, clk, code, out_ready, out)
    print("Num components:", circ.num_components())

    while True:
        circ.stabilize()

        if out_ready.get() and clk.get():
            print(wires_to_num(out))

        # cpu.snapshot()
        clk.put(OSCILLATOR, 1 - clk.get())
