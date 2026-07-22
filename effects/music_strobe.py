import time
import random
import numpy as np
import sounddevice as sd
from effects.base import Effect


class SparklePulse:
    """Ein einzelner Glitzer-Blitz an einer bestimmten Position des Strips."""

    def __init__(self, center_pos, color, max_brightness=1.0):
        self.center_pos = center_pos  # Haupt-LED (Mitte des Blitzes)
        self.color = color  # (R, G, B)
        self.brightness = max_brightness


class MusicStrobeEffect(Effect):
    def __init__(self, name="Music Strobe Sparkle", colors=None,
                 enable_white_strobe=True, enable_afterglow=True, sensitivity=2.5, decay=0.80):
        super().__init__(name=name)

        # Standard: 2 Farben (z.B. Rot & Gelb)
        self.colors = colors if colors else [(255, 0, 0), (255, 255, 0)]
        self.enable_white_strobe = enable_white_strobe  # Weißes Blitzen an/aus
        self.enable_afterglow = enable_afterglow
        self.sensitivity = sensitivity
        self.decay = decay  # Ausfadedauer der Glitzerpunkte (0.6 = sehr schnell, 0.85 = langsamer)

        self.sample_rate = 44100
        self.chunk_size = 1024

        self.active_sparkles = []
        self.last_beat_time = 0.0
        self.beat_cooldown = 0.08  # Mindestabstand zwischen Beat-Triggern (in Sekunden)

        # Audio Stream starten
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()

    def _audio_callback(self, indata, frames, time_info, status):
        now = time.time()
        audio = indata[:, 0]

        # Lautstärke-Pegel (RMS)
        rms = np.sqrt(np.mean(audio ** 2))
        vol = rms * self.sensitivity * 7.0

        # Beat-Trigger erkennen
        if vol > 0.4 and (now - self.last_beat_time) > self.beat_cooldown:
            self.last_beat_time = now
            self._spawn_beat_sparkles(vol)

    def _spawn_beat_sparkles(self, volume):
        """Erzeugt bei einem Beat mehrere Glitzerpunkte verteilt über den Strip."""
        num_sparkles = random.randint(4, 8)  # 3 bis 6 Glitzer-Cluster pro Beat Drop

        for _ in range(num_sparkles):
            # Entscheiden, ob dieser Blitz weiß wird (falls Option aktiv) oder eine Farbwahl trifft
            if self.enable_white_strobe and random.random() < 0.35:
                color = (255, 255, 255)  # Helles Weiß
            else:
                color = random.choice(self.colors)

            # Zufällige Position auf dem Strip wählen (wird im update skaliert)
            pos_ratio = random.random()
            self.active_sparkles.append(SparklePulse(center_pos=pos_ratio, color=color))

    def update(self, strip):
        num_leds = strip.num_leds

        # Strip leeren (Schwarzer Hintergrund)
        strip.set_all(0, 0, 0)

        # Buffer für Farbwerte (R, G, B) pro LED initialisieren
        rgb_buffer = np.zeros((num_leds, 3), dtype=float)

        surviving_sparkles = []

        for sparkle in self.active_sparkles:
            if sparkle.brightness <= 0.02:
                continue  # Sparkle verblassen lassen & verwerfen

            surviving_sparkles.append(sparkle)

            # Echte LED-Indexposition berechnen
            center = int(sparkle.center_pos * num_leds)

            # 2 bis 3 Haupt-LEDs extrem hell + außenrum gefadet
            # Radius 2 bedeutet: -2, -1, 0 (Mitte), +1, +2 (insgesamt 5 LEDs Abdeckung)
            for offset in [-2, -1, 0, 1, 2]:
                led_idx = center + offset
                if 0 <= led_idx < num_leds:
                    # Dämpfung nach außen (Mitte = 1.0, direkt daneben = 0.6, ganz außen = 0.2)
                    if offset == 0:
                        falloff = 1.0
                    elif abs(offset) == 1:
                        falloff = 0.65
                    else:
                        falloff = 0.25

                    intensity = sparkle.brightness * falloff

                    # In den Buffer einrechnen (Farbe * Intensität)
                    rgb_buffer[led_idx][0] += sparkle.color[0] * intensity
                    rgb_buffer[led_idx][1] += sparkle.color[1] * intensity
                    rgb_buffer[led_idx][2] += sparkle.color[2] * intensity

            # Sparkle für den nächsten Frame ausfaden lassen
            sparkle.brightness *= self.decay

        self.active_sparkles = surviving_sparkles

        # Buffer-Werte auf max 255 begrenzen und auf den Strip schreiben
        for i in range(num_leds):
            r = int(min(255, rgb_buffer[i][0]))
            g = int(min(255, rgb_buffer[i][1]))
            b = int(min(255, rgb_buffer[i][2]))
            if r > 0 or g > 0 or b > 0:
                strip.set_pixel(i, r, g, b)

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()