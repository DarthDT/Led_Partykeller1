import time
import math
import numpy as np
import sounddevice as sd
from effects.base import Effect


class MusicRunnerEffect(Effect):
    def __init__(self, name="Music Runner", direction="edges_to_center",
                 color_mode="rainbow", solid_color=(255, 0, 0), custom_colors=None,
                 speed=2.0, fadeout_sec=3.0, base_brightness=0.3, enable_music=True, sensitivity=2.5):
        super().__init__(name=name)

        # Einstellungen
        self.direction = direction  # 'left_to_right', 'right_to_left', 'edges_to_center', 'center_to_edges'
        self.color_mode = color_mode  # 'solid', 'custom_gradient', 'rainbow'
        self.solid_color = solid_color
        self.custom_colors = custom_colors if custom_colors else [(255, 0, 0), (0, 0, 255)]

        self.speed = speed  # Geschwindigkeit, mit der die Farbe wandert
        self.fadeout_sec = fadeout_sec  # Fadeout-Dauer (bestimmt wie lange das Licht beim Weiterlaufen nachleuchtet)
        self.base_brightness = base_brightness  # Grundhelligkeit am Ursprung (0.1 bis 0.9)
        self.enable_music = enable_music  # Musikreaktion An/Aus
        self.sensitivity = sensitivity

        # Interner Zustand
        self.position = 0.0
        self.current_volume = 0.0  # Geglätteter Lautstärke-Pegel
        self.led_buffer = None
        self.last_update_time = time.time()

        # Audio Stream initialisieren
        self.sample_rate = 44100
        self.chunk_size = 1024

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.chunk_size,
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()

    def _audio_callback(self, indata, frames, time_info, status):
        if not self.enable_music:
            self.current_volume = 0.0
            return

        audio = indata[:, 0]
        rms = np.sqrt(np.mean(audio ** 2))
        vol = rms * self.sensitivity * 5.0

        # Lautstärkesignal direkt aufnehmen (0.0 bis 1.0)
        self.current_volume = min(1.0, max(0.0, vol))

    def _get_color(self, pos_ratio):
        """Ermittelt die Farbe basierend auf Position und eingestelltem Modus."""
        if self.color_mode == "solid":
            return self.solid_color

        elif self.color_mode == "rainbow":
            hue = (pos_ratio + time.time() * 0.2) % 1.0
            r, g, b = [int(c * 255) for c in self._hue_to_rgb(hue)]
            return (r, g, b)

        elif self.color_mode == "custom_gradient":
            num_colors = len(self.custom_colors)
            if num_colors == 1:
                return self.custom_colors[0]

            scaled_pos = (pos_ratio % 1.0) * (num_colors - 1)
            idx1 = int(scaled_pos)
            idx2 = min(idx1 + 1, num_colors - 1)
            blend = scaled_pos - idx1

            c1 = self.custom_colors[idx1]
            c2 = self.custom_colors[idx2]

            r = int(c1[0] * (1 - blend) + c2[0] * blend)
            g = int(c1[1] * (1 - blend) + c2[1] * blend)
            b = int(c1[2] * (1 - blend) + c2[2] * blend)
            return (r, g, b)

        return (255, 255, 255)

    @staticmethod
    def _hue_to_rgb(h):
        i = int(h * 6.0)
        f = (h * 6.0) - i
        q = 1.0 - f
        if i % 6 == 0: return 1.0, f, 0.0
        if i % 6 == 1: return q, 1.0, 0.0
        if i % 6 == 2: return 0.0, 1.0, f
        if i % 6 == 3: return 0.0, q, 1.0
        if i % 6 == 4: return f, 0.0, 1.0
        if i % 6 == 5: return 1.0, 0.0, q
        return 0.0, 0.0, 0.0

    def update(self, strip):
        num_leds = strip.num_leds
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        if self.led_buffer is None or len(self.led_buffer) != num_leds:
            self.led_buffer = np.zeros((num_leds, 3), dtype=float)

        # 1. Das gesamte Lichtband um die konstante Fadeout-Rate abklingen lassen
        decay_rate = math.pow(0.01, dt / max(1.0, self.fadeout_sec))
        self.led_buffer *= decay_rate

        # 2. Die Bewegungsposition des "Einspeisepunkts" weiterschalten
        self.position = (self.position + self.speed * dt * 30.0) % num_leds
        head_idx = int(self.position)

        # 3. Einspeise-Helligkeit berechnen:
        # Bei leiser Musik = Grundhelligkeit -> Fadeout lässt das Licht schnell erlöschen (Reichweite kurz)
        # Bei lautem Beat = Bis zu 100% Helligkeit -> Durch den gleichen Decay reicht das Licht VIEL weiter!
        if self.enable_music:
            source_brightness = min(1.0, self.base_brightness + self.current_volume * (1.0 - self.base_brightness))
        else:
            source_brightness = self.base_brightness

        # 4. Ursprungspunkte je nach gewählter Laufrichtung ermitteln
        origins = []

        if self.direction == "left_to_right":
            origins.append(0)  # Ursprung links
        elif self.direction == "right_to_left":
            origins.append(num_leds - 1)  # Ursprung rechts
        elif self.direction == "edges_to_center":
            origins.append(0)  # Von den beiden Außenkanten...
            origins.append(num_leds - 1)  # ...nach innen
        elif self.direction == "center_to_edges":
            center = num_leds // 2
            origins.append(center)  # Von der Mitte nach außen

        # 5. Helles Signal am Ursprung einspeisen
        for origin_idx in origins:
            if 0 <= origin_idx < num_leds:
                pos_ratio = (head_idx / num_leds)
                color = self._get_color(pos_ratio)

                self.led_buffer[origin_idx][0] = color[0] * source_brightness
                self.led_buffer[origin_idx][1] = color[1] * source_brightness
                self.led_buffer[origin_idx][2] = color[2] * source_brightness

        # 6. Verschieben/Fortpflanzen des Lichts entlang des Strips in die gewählte Richtung
        # (Schiebt die RGB-Werte Schritt für Schritt weiter)
        shift_amount = self.speed * dt * 25.0
        if shift_amount >= 0.5:
            if self.direction == "left_to_right":
                self.led_buffer[1:] = self.led_buffer[:-1]
            elif self.direction == "right_to_left":
                self.led_buffer[:-1] = self.led_buffer[1:]
            elif self.direction == "edges_to_center":
                half = num_leds // 2
                self.led_buffer[1:half] = self.led_buffer[0:half - 1]
                self.led_buffer[half:-1] = self.led_buffer[half + 1:]
            elif self.direction == "center_to_edges":
                half = num_leds // 2
                self.led_buffer[0:half] = self.led_buffer[1:half + 1]
                self.led_buffer[half + 1:] = self.led_buffer[half:-1]

        # 7. Auf den LED-Strip schreiben
        for i in range(num_leds):
            strip.set_pixel(
                i,
                int(min(255, self.led_buffer[i][0])),
                int(min(255, self.led_buffer[i][1])),
                int(min(255, self.led_buffer[i][2]))
            )

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()