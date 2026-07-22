import time
from effects.base import Effect
from hardware.audio_input import AudioAnalyzer


class VuMeterEffect(Effect):
    def __init__(self, name="Audio VU-Meter Center", color_mode="gradient",
                 solid_color=(0, 255, 0), gradient_colors=None,
                 peak_color=(255, 0, 0), sensitivity=1.5):
        super().__init__(name=name)

        self.color_mode = color_mode  # "solid" oder "gradient"
        self.solid_color = solid_color
        self.gradient_colors = gradient_colors if gradient_colors else [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
        self.peak_color = peak_color
        self.sensitivity = sensitivity  # Empfindlichkeit / Gain

        # Peak Hold Logik
        self.peak_pos = 0.0  # Aktuelle LED-Position des Peaks
        self.last_peak_time = 0.0  # Zeitpunkt des letzten neuen Maxima
        self.peak_hold_sec = 0.5  # Haltezeit
        self.peak_fall_speed = 12.0  # LEDs pro Sekunde beim Abfallen

        # Audio Analyzer instanziieren
        self.audio = AudioAnalyzer()
        self.audio.start()
        self.last_update = time.time()

    def _interpolate_color(self, c1, c2, factor):
        factor = max(0.0, min(1.0, factor))
        r = int(c1[0] + (c2[0] - c1[0]) * factor)
        g = int(c1[1] + (c2[1] - c1[1]) * factor)
        b = int(c1[2] + (c2[2] - c1[2]) * factor)
        return (r, g, b)

    def _get_bar_color(self, progress):
        """progress: 0.0 (Mitte) bis 1.0 (Rand)"""
        if self.color_mode == "solid":
            return self.solid_color
        else:
            # Gradient über die Balkenlänge
            num_cols = len(self.gradient_colors)
            if num_cols == 2:
                return self._interpolate_color(self.gradient_colors[0], self.gradient_colors[1], progress)
            else:
                if progress < 0.5:
                    return self._interpolate_color(self.gradient_colors[0], self.gradient_colors[1], progress * 2.0)
                else:
                    return self._interpolate_color(self.gradient_colors[1], self.gradient_colors[2],
                                                   (progress - 0.5) * 2.0)

    def update(self, strip):
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # Lautstärke abfragen & skalieren
        vol = self.audio.get_volume() * self.sensitivity
        vol = max(0.0, min(1.0, vol))

        half_strip = strip.num_leds // 2
        center = half_strip

        # Aktuelle Ausschlag-Länge in LEDs von der Mitte aus
        current_led_count = int(vol * half_strip)

        # --- PEAK-HOLD LOGIK ---
        if current_led_count >= self.peak_pos:
            self.peak_pos = float(current_led_count)
            self.last_peak_time = now
        else:
            # 0.5 Sekunden gewartet? Dann langsam abfallen lassen
            if now - self.last_peak_time > self.peak_hold_sec:
                self.peak_pos -= self.peak_fall_speed * dt
                if self.peak_pos < current_led_count:
                    self.peak_pos = float(current_led_count)

        # Alles löschen
        strip.set_all(0, 0, 0)

        # --- BALKEN VON DER MITTE NACH AUSSEN ZEICHNEN ---
        for i in range(current_led_count):
            progress = i / max(1, half_strip - 1)
            r, g, b = self._get_bar_color(progress)

            # Rechts von der Mitte
            if center + i < strip.num_leds:
                strip.set_pixel(center + i, r, g, b)
            # Links von der Mitte
            if center - 1 - i >= 0:
                strip.set_pixel(center - 1 - i, r, g, b)

        # --- PEAK PUNKT ZEICHNEN ---
        peak_idx = int(self.peak_pos)
        if peak_idx > 0:
            pr, pg, pb = self.peak_color
            # Peak Rechts
            if center + peak_idx - 1 < strip.num_leds:
                strip.set_pixel(center + peak_idx - 1, pr, pg, pb)
            # Peak Links
            if center - peak_idx >= 0:
                strip.set_pixel(center - peak_idx, pr, pg, pb)