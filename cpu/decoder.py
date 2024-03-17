from cmp import Equals, MultiEquals


def Decoder(
    circuit,
    in_inst,
    out_is_fwd,
    out_is_bwd,
    out_is_inc,
    out_is_dec,
    out_is_jnz,
    out_is_prnt,
):
    MultiEquals(
        circuit,
        in_inst[0:4],
        [circuit.zero(), circuit.zero(), circuit.zero(), circuit.zero()],
        out_is_fwd,
    )
    MultiEquals(
        circuit,
        in_inst[0:4],
        [circuit.zero(), circuit.one(), circuit.zero(), circuit.zero()],
        out_is_bwd,
    )
    MultiEquals(
        circuit,
        in_inst[0:4],
        [circuit.zero(), circuit.zero(), circuit.one(), circuit.zero()],
        out_is_inc,
    )
    MultiEquals(
        circuit,
        in_inst[0:4],
        [circuit.zero(), circuit.one(), circuit.one(), circuit.zero()],
        out_is_dec,
    )
    MultiEquals(
        circuit,
        in_inst[0:4],
        [circuit.zero(), circuit.zero(), circuit.zero(), circuit.one()],
        out_is_prnt,
    )
    Equals(circuit, in_inst[0], circuit.one(), out_is_jnz)
