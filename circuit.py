from wire import Wire, ONE, ZERO


class Circuit:
    def __init__(self):
        self._wires = []
        self._comps = []

        self._zero = self.new_wire()
        self._zero.put(self, ZERO)
        self._one = self.new_wire()
        self._one.put(self, ONE)

    def one(self):
        return self._one

    def zero(self):
        return self._zero

    def new_wire(self):
        w = Wire()
        self._wires.append(w)
        return w

    def add_component(self, comp):
        self._comps.append(comp)

    def num_components(self):
        return len(self._comps)

    def update(self):
        has_changes = False
        for t in self._comps:
            has_changes = has_changes | t.update()
        return has_changes

    def stabilize(self):
        while self.update():
            pass
