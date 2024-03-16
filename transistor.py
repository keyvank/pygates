from wire import *


class NTransistor:
    def __init__(self, circuit, wire_base, wire_emitter, wire_collector):
        self.wire_base = wire_base
        self.wire_emitter = wire_emitter
        self.wire_collector = wire_collector

    def is_ready(self):
        return self.wire_base.get() != FREE

    def update(self):
        b = self.wire_base.get()
        if b == ONE:
            self.wire_collector.put(self, self.wire_emitter.get())
        elif b == ZERO:
            self.wire_collector.put(self, FREE)
        else:
            self.wire_collector.put(self, UNK)


class PTransistor:
    def __init__(self, circuit, wire_base, wire_emitter, wire_collector):
        self.wire_base = wire_base
        self.wire_emitter = wire_emitter
        self.wire_collector = wire_collector

    def is_ready(self):
        return self.wire_base.get() != FREE

    def update(self):
        b = self.wire_base.get()
        if b == ZERO:
            self.wire_collector.put(self, self.wire_emitter.get())
        elif b == ONE:
            self.wire_collector.put(self, FREE)
        else:
            self.wire_collector.put(self, UNK)
