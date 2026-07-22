import sys
import time
import pygame


class LEDStripSimulator:
    def __init__(self, num_leds=60, led_radius=6, spacing=3):
        """
        Initialisiert den Pygame-LED-Simulator.
        :param num_leds: Anzahl der simulierten LEDs im Strip
        :param led_radius: Radius jeder LED im Fenster (in Pixeln)
        :param spacing: Abstand zwischen den LEDs (in Pixeln)
        """
        self.num_leds = num_leds
        self.led_radius = led_radius
        self.spacing = spacing

        # Interne Liste für die RGB-Farben aller LEDs: [(R, G, B), (R, G, B), ...]
        self.pixels = [(0, 0, 0)] * self.num_leds

        # Fensterbreite dynamisch basierend auf LED-Anzahl berechnen
        window_width = self.num_leds * (self.led_radius * 2 + self.spacing) + self.spacing + 20
        window_height = 100

        # Pygame-Fenster initialisieren
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Partykeller ARGB LED Simulator")
        self.clock = pygame.time.Clock()

    def set_pixel(self, index, r, g, b):
        """Setzt die Farbe einer einzelnen LED an der Position 'index' (0 bis num_leds - 1)."""
        if 0 <= index < self.num_leds:
            # Werte auf den gültigen RGB-Bereich (0-255) begrenzen
            r = max(0, min(255, int(r)))
            g = max(0, min(255, int(g)))
            b = max(0, min(255, int(b)))
            self.pixels[index] = (r, g, b)

    def set_all(self, r, g, b):
        """Setzt alle LEDs im Strip auf dieselbe RGB-Farbe."""
        for i in range(self.num_leds):
            self.set_pixel(i, r, g, b)

    def show(self):
        """
        Rendert den aktuellen LED-Zustand ins Pygame-Fenster.
        Fängt außerdem das Schließen-Event des Fensters ab.
        """
        # Event-Queue abarbeiten, damit das Fenster ansprechbar bleibt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dunkelgrauer Hintergrund
        self.screen.fill((20, 20, 20))

        # LEDs zeichnen
        y_pos = 50
        for i, color in enumerate(self.pixels):
            x_pos = 15 + i * (self.led_radius * 2 + self.spacing) + self.led_radius

            # Dunkler Gehäuserand der LED
            pygame.draw.circle(self.screen, (50, 50, 50), (x_pos, y_pos), self.led_radius + 2)
            # Eigentliche LED-Farbe
            pygame.draw.circle(self.screen, color, (x_pos, y_pos), self.led_radius)

        pygame.display.flip()


# =========================================================
# TEST-SKRIP (wird nur ausgeführt, wenn du die Datei direkt startest)
# =========================================================
if __name__ == "__main__":
    # Erstelle einen Test-Strip mit 150 LEDs
    strip = LEDStripSimulator(num_leds=150)

    print("Simulator gestartet! Schließe das Fenster zum Beenden.")

    # Ein einfaches Test-Lauflicht
    position = 0
    while True:
        # Alle LEDs auf Schwarz (aus)
        strip.set_all(0, 0, 0)

        # Eine rote LED weiterwandern lassen
        strip.set_pixel(position, 0, 155, 155)

        # Aktualisiert das Fenster
        strip.show()

        # Position für nächsten Durchlauf hochzählen
        position = (position + 1) % strip.num_leds

        # Kurze Pause (20 Bps / Frames pro Sekunde)
        time.sleep(0.05)