import os
import time
import tkinter as tk

import pygame

from core.preset_manager import PresetManager
from gui import ControlPanelGUI

# Hardware & Combined Imports
from hardware.simulator import LEDStripSimulator
from hardware.ws2812 import LEDStripHardware
from hardware.combined import CombinedLEDStrip

# Effekte
from effects.solid import SolidEffect
from effects.chase import ChaseEffect
from effects.wave import WaveEffect
from effects.gradient import GradientEffect
from effects.vu_meter import VuMeterEffect
from effects.music_strobe import MusicStrobeEffect
from effects.music_runner import MusicRunnerEffect


def main():
    # 1. Beide Strips initialisieren
    sim_strip = LEDStripSimulator(num_leds=150)
    hw_strip = LEDStripHardware(num_leds=150, pin=18)

    # 2. Im CombinedLEDStrip bündeln
    strip = CombinedLEDStrip(sim_strip, hw_strip)

    # 3. Manager & Effekte einrichten
    manager = PresetManager()
    manager.add_preset("solid_color", SolidEffect(name="Dauerleuchten", r=255, g=0, b=0))
    manager.add_preset("chase_effect", ChaseEffect(
        name="Lauflicht Dynamisch",
        head_color=(255, 0, 0),
        tail_color=(255, 255, 0),
        head_length=3,
        tail_length=5,
        num_objects=4
    ))
    manager.add_preset("wave_effect", WaveEffect(
        name="Wabernder Ozean",
        colors=[(255, 0, 0), (255, 255, 0)],
        speed=0.02,
        scale=0.04,
        contrast=1.5
    ))
    manager.add_preset("gradient_effect", GradientEffect(name="Farbübergang", is_rainbow=True))
    manager.add_preset("vu_meter", VuMeterEffect(name="VU-Meter"))
    manager.add_preset("music_strobe", MusicStrobeEffect(name="Music-Strobe"))
    manager.add_preset("music_runner", MusicRunnerEffect(name="Music-Runner"))

    # 4. Tkinter GUI starten
    gui = ControlPanelGUI(manager)

    # 5. Hauptschleife
    running = True
    while running:
        # Tkinter GUI-Events verarbeiten
        try:
            gui.update()
        except tk.TclError:
            break

        # Pygame Window-Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aktiven Effekt aktualisieren
        current_effect = manager.get_active_effect()
        if current_effect:
            current_effect.update(strip)

        # Rendert sowohl das Pygame-Fenster als auch die GPIO 18 LEDs
        strip.show()
        time.sleep(0.01)

    pygame.quit()


if __name__ == "__main__":
    main()