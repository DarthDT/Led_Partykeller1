import time
from effects.base import Effect


class ChaseEffect(Effect):
    def __init__(self, name="Lauflicht", head_color=(255, 0, 0), tail_color=(0, 0, 255),
                 speed=0.03, tail_length=5, head_length=1, num_objects=1):
        super().__init__(name=name)
        self.head_color = head_color  # RGB-Tupel für den Kopf
        self.tail_color = tail_color  # RGB-Tupel für das Schweifende
        self.speed = speed
        self.tail_length = tail_length
        self.head_length = head_length
        self.num_objects = num_objects

        self.position = 0
        self.last_update = time.time()

    def _interpolate_color(self, c1, c2, factor):
        """Mischt sanft von Farbe c1 zu Farbe c2 basierend auf factor (0.0 bis 1.0)."""
        factor = max(0.0, min(1.0, factor))
        r = int(c1[0] + (c2[0] - c1[0]) * factor)
        g = int(c1[1] + (c2[1] - c1[1]) * factor)
        b = int(c1[2] + (c2[2] - c1[2]) * factor)
        return (r, g, b)

    def update(self, strip):
        current_time = time.time()

        # Position weiterschalten
        if current_time - self.last_update >= self.speed:
            self.position = (self.position + 1) % strip.num_leds
            self.last_update = current_time

        strip.set_all(0, 0, 0)
        spacing = strip.num_leds // max(1, self.num_objects)

        for obj in range(self.num_objects):
            base_pos = (self.position + obj * spacing) % strip.num_leds

            # 1. Hauptköpfe (Head Length) -> In Head-Farbe
            for h in range(self.head_length):
                pos = (base_pos - h) % strip.num_leds
                strip.set_pixel(pos, *self.head_color)

            # 2. Schweif (Tail Length) -> Sanfter Fade von Head-Farbe zu Tail-Farbe & Ausfaden
            if self.tail_length > 0:
                for t in range(1, self.tail_length + 1):
                    pos = (base_pos - self.head_length + 1 - t) % strip.num_leds

                    # Farbverlauf von Head-Farbe nach Tail-Farbe
                    color_factor = t / self.tail_length
                    faded_color = self._interpolate_color(self.head_color, self.tail_color, color_factor)

                    # Zusätzlich Helligkeit nach hinten abfallen lassen
                    brightness_factor = max(0.0, 1.0 - (t / (self.tail_length + 1)))
                    r = int(faded_color[0] * brightness_factor)
                    g = int(faded_color[1] * brightness_factor)
                    b = int(faded_color[2] * brightness_factor)

                    strip.set_pixel(pos, r, g, b)