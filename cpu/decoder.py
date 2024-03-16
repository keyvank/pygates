from cmp import Equals, MultiEquals


def Decoder(circuit, instruction, is_fwd, is_bwd, is_inc, is_dec, is_jmp):
    MultiEquals(
        circuit,
        instruction[0:3],
        [circuit.zero(), circuit.zero(), circuit.zero()],
        is_fwd,
    )
    MultiEquals(
        circuit,
        instruction[0:3],
        [circuit.zero(), circuit.one(), circuit.zero()],
        is_bwd,
    )
    MultiEquals(
        circuit,
        instruction[0:3],
        [circuit.zero(), circuit.zero(), circuit.one()],
        is_inc,
    )
    MultiEquals(
        circuit,
        instruction[0:3],
        [circuit.zero(), circuit.one(), circuit.one()],
        is_dec,
    )
    Equals(circuit, instruction[0], circuit.one(), is_jmp)
