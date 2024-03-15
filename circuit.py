from wire import Wire, FREE, ZERO, UNK


class Circuit:
    def __init__(self):
        self._one = Wire.one()
        self._zero = Wire.zero()
        self._wires = []
        self._transistors = []

    def one(self):
        return self._one

    def zero(self):
        return self._zero

    def new_wire(self):
        w = Wire()
        self._wires.append(w)
        return w

    def new_transistor(self, trans):
        self._transistors.append(trans)

    def snapshot(self):
        return [w.get() for w in self._wires]

    def update(self):
        for t in self._transistors:
            if t.is_ready():
                t.update()

    def stabilize(self):
        self.update()
        self.update()
        # curr_snapshot = self.snapshot()
        # next_snapshot = None
        # while next_snapshot != curr_snapshot:
        #    self.update()
        #    curr_snapshot = next_snapshot
        #    next_snapshot = self.snapshot()
