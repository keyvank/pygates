from wire import *


class NTransistor:
    def __init__(self, circuit, wire_base, wire_collector, wire_emitter):
        self.wire_base = wire_base
        self.wire_collector = wire_collector
        self.wire_emitter = wire_emitter

    def update(self):
        b = self.wire_base.get()
        if b == ONE:
            self.wire_emitter.put(self, self.wire_collector.get())
        elif b == ZERO:
            self.wire_emitter.put(self, FREE)
        elif b == UNK:
            self.wire_emitter.put(self, UNK)
        else:
            return False

        return True


class PTransistor:
    def __init__(self, circuit, wire_base, wire_collector, wire_emitter):
        self.wire_base = wire_base
        self.wire_collector = wire_collector
        self.wire_emitter = wire_emitter

    def update(self):
        b = self.wire_base.get()
        if b == ZERO:
            self.wire_emitter.put(self, self.wire_collector.get())
        elif b == ONE:
            self.wire_emitter.put(self, FREE)
        elif b == UNK:
            self.wire_emitter.put(self, UNK)
        else:
            return False

        return True
