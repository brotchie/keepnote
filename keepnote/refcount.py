


class RefCount (object):

    def __init__(self, on_zero):
        self._count = 0
        self._value = value
        self._on_zero = on_zero

    def inc(self, inc):
        self._count += inc

    def dec(self, dec):
        self._count -= dec
        if self._count <= 0:
            self._on_zero()


