from wire import Wire
from utils import num_to_wires, wires_to_num
from circuit import Circuit
from adder import Adder8


if __name__ == "__main__":
    for x in range(256):
        for y in range(256):
            circuit = Circuit()
            wires_x = num_to_wires(x)
            wires_y = num_to_wires(y)
            wires_out = [Wire() for _ in range(8)]
            Adder8(circuit, wires_x, wires_y, Wire.zero(), wires_out, Wire.zero())
            circuit.update()
            out = wires_to_num(wires_out)
            if out != (x + y) % 256:
                print("Adder is not working!")
