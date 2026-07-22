from effects.base import Effect

class SolidEffect(Effect):
    def __init__(self, name="Solid Color", r=255, g=0, b=0):
        super().__init__(name=name)
        self.r = r
        self.g = g
        self.b = b

    def update(self, strip):
        strip.set_all(self.r, self.g, self.b)