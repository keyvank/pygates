from wire import Wire


class Circuit:
    def __init__(self):
        self._one = Wire.one()
        self._zero = Wire.zero()
        self._wires = []

    def one(self):
        return self._one

    def zero(self):
        return self._zero

    def new_wire(self):
        w = Wire()
        self._wires.append(w)
        return w
