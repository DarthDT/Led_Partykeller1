import time
from effects.base import Effect


class GradientEffect(Effect):
    # Fertiges Regenbogen-Preset
    RAINBOW_COLORS = [
        (255, 0, 0),  # Rot
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Gelb
        (0, 255, 0),  # Grün
        (0, 0, 255),  # Blau
        (75, 0, 130),  # Indigo
        (148, 0, 211)  # Violett
    ]

    def __init__(self, name="Farbverlauf", colors=None, speed=0.02, repeat=1.0, is_rainbow=False):
        super().__init__(name=name)

        self.is_rainbow = is_rainbow
        if is_rainbow:
            self.colors = list(self.RAINBOW_COLORS)
        else:
            self.colors = colors if colors else [(255, 0, 0), (0, 0, 255)]  # Standard: Rot -> Blau

        self.speed = speed  # Geschwindigkeit des Wanderns
        self.repeat = repeat  # Wie oft sich das Muster über die Gesamtlänge wiederholt
        self.offset = 0.0
        self.last_update = time.time()

    def set_rainbow_mode(self, active: bool):
        self.is_rainbow = active
        if active:
            self.colors = list(self.RAINBOW_COLORS)

    def set_custom_colors(self, new_colors):
        if 2 <= len(new_colors) <= 4:
            self.is_rainbow = False
            self.colors = new_colors

    def _interpolate_multi_color(self, factor):
        """Berechnet die Farbe an einem Punkt (0.0 bis 1.0) über N Farben hinweg."""
        factor = factor % 1.0
        num_colors = len(self.colors)

        # Aufteilung der Abschnitte zwischen den Farben
        scaled_factor = factor * num_colors
        idx1 = int(scaled_factor) % num_colors
        idx2 = (idx1 + 1) % num_colors

        local_factor = scaled_factor - int(scaled_factor)

        c1 = self.colors[idx1]
        c2 = self.colors[idx2]

        r = int(c1[0] + (c2[0] - c1[0]) * local_factor)
        g = int(c1[1] + (c2[1] - c1[1]) * local_factor)
        b = int(c1[2] + (c2[2] - c1[2]) * local_factor)

        return (r, g, b)

    def update(self, strip):
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # Offset verschieben für die Animation
        self.offset = (self.offset + dt * self.speed * 5.0) % 1.0

        for i in range(strip.num_leds):
            # Position auf dem Strip (0.0 bis 1.0) unter Berücksichtigung der Wiederholungen
            pos_factor = ((i / strip.num_leds) * self.repeat + self.offset) % 1.0
            r, g, b = self._interpolate_multi_color(pos_factor)
            strip.set_pixel(i, r, g, b)