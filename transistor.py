from wire import *


class NTransistor:
    def __init__(self, in_base, in_collector, out_emitter):
        self.in_base = in_base
        self.in_collector = in_collector
        self.out_emitter = out_emitter

    def update(self):
        b = self.in_base.get()
        if b == ONE:
            return self.out_emitter.put(self, self.in_collector.get())
        elif b == ZERO:
            return self.out_emitter.put(self, FREE)
        elif b == UNK:
            return self.out_emitter.put(self, UNK)
        else:
            return True  # Trigger re-update


class PTransistor:
    def __init__(self, in_base, in_collector, out_emitter):
        self.in_base = in_base
        self.in_collector = in_collector
        self.out_emitter = out_emitter

    def update(self):
        b = self.in_base.get()
        if b == ZERO:
            return self.out_emitter.put(self, self.in_collector.get())
        elif b == ONE:
            return self.out_emitter.put(self, FREE)
        elif b == UNK:
            return self.out_emitter.put(self, UNK)
        else:
            return True  # Trigger re-update
