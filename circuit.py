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

    def is_stable(self):
        for w in self._wires:
            if w.get() in [FREE, UNK]:
                return False
        return True

    def update(self):
        for t in self._transistors:
            t.update()

    def stabilize(self):
        self.update()        
        while not self.is_stable():
            self.update()
