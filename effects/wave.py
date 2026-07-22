import time
import math
from perlin_noise import PerlinNoise
from effects.base import Effect


class WaveEffect(Effect):
    def __init__(self, name="Wabernde Farben", colors=None, speed=0.02, scale=0.03, contrast=2.5):
        super().__init__(name=name)

        self.colors = colors if colors else [(0, 200, 255), (0, 10, 120)]
        self.speed = speed
        self.scale = scale
        self.contrast = contrast  # 👈 Steuert die Stärke/Schärfe der Übergänge (1.0 = weich, 4.0 = stark)

        self.noise = PerlinNoise(octaves=2)
        self.time_offset = 0.0
        self.last_update = time.time()

    def set_colors(self, new_colors):
        if 2 <= len(new_colors) <= 3:
            self.colors = new_colors

    def _interpolate_color(self, c1, c2, factor):
        factor = max(0.0, min(1.0, factor))
        r = int(c1[0] + (c2[0] - c1[0]) * factor)
        g = int(c1[1] + (c2[1] - c1[1]) * factor)
        b = int(c1[2] + (c2[2] - c1[2]) * factor)
        return (r, g, b)

    def _apply_contrast(self, val):
        """Erhöht den Kontrast des Perlin-Noise Wertebereichs (S-Kurve/Sigmoid)."""
        # Normieren auf 0.0 bis 1.0
        norm = max(0.0, min(1.0, val + 0.5))

        # S-Kurven-Transformation um den Mittelpunkt 0.5 herum
        if self.contrast <= 1.0:
            return norm

        # Zieht Mittelwerte zu den Extremen (0.0 und 1.0) für kräftigere Farben
        centered = norm - 0.5
        adjusted = math.copysign(abs(centered) ** (1.0 / self.contrast), centered)
        return adjusted + 0.5

    def _get_color_from_val(self, val):
        # Kontrast anwenden
        norm_val = self._apply_contrast(val)

        num_colors = len(self.colors)

        if num_colors <= 2:
            return self._interpolate_color(self.colors[0], self.colors[1], norm_val)
        else:
            if norm_val < 0.5:
                factor = norm_val * 2.0
                return self._interpolate_color(self.colors[0], self.colors[1], factor)
            else:
                factor = (norm_val - 0.5) * 2.0
                return self._interpolate_color(self.colors[1], self.colors[2], factor)

    def update(self, strip):
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        self.time_offset += dt * self.speed * 50.0

        for i in range(strip.num_leds):
            noise_val = self.noise([i * self.scale, self.time_offset])
            r, g, b = self._get_color_from_val(noise_val)
            strip.set_pixel(i, r, g, b)