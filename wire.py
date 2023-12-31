FREE = "Z"
UNK = "X"
ZERO = "0"
ONE = "1"

BATTERY = None


class Wire:
    def __init__(self):
        self.values = {}

    def one():
        w = Wire()
        w.put(BATTERY, ONE)
        return w

    def zero():
        w = Wire()
        w.put(BATTERY, ZERO)
        return w

    def get(self):
        curr = FREE
        for b in self.values.values():
            if b == UNK:
                return UNK
            elif b != FREE:
                if curr == FREE:
                    curr = b
                elif b != curr:
                    return UNK
        return curr

    def put(self, gate, value):
        self.values[gate] = value
