# hardware/ws2812.py

# Versuche die Raspberry-Pi-spezifische Bibliothek zu laden
try:
    from rpi_ws281x import PixelStrip, Color

    HAS_HARDWARE = True
except (ImportError, RuntimeError):
    HAS_HARDWARE = False
    print("⚠️ rpi_ws281x nicht gefunden/unterstützt (PC-Modus aktiv). Fallback geladen.")


class LEDStripHardware:
    def __init__(self, num_leds=60, pin=18, brightness=255, channel=0):
        """
        Initialisiert den echten WS2812B / ARGB Strip oder den Fallback-Puffer am PC.
        :param num_leds: Anzahl der LEDs
        :param pin: GPIO-Pin des Pi (Standard: 18 / PWM0)
        :param brightness: Helligkeit (0-255)
        :param channel: PWM-Kanal (0 für GPIO 18)
        """
        self.num_leds = num_leds
        self.pin = pin

        if HAS_HARDWARE:
            # rpi_ws281x Hardware-Konfiguration (800kHz Frequenz, DMA Kanal 10)
            self.strip = PixelStrip(num_leds, pin, 800000, 10, False, brightness, channel)
            self.strip.begin()
        else:
            # Virtueller Speicher-Puffer für Tests auf dem PC
            self.pixels = [(0, 0, 0)] * num_leds

    def set_pixel(self, index: int, color: tuple):
        """Setzt eine einzelne LED (Farbe als RGB-Tuple: z.B. (255, 0, 0))."""
        if 0 <= index < self.num_leds:
            r, g, b = color
            if HAS_HARDWARE:
                self.strip.setPixelColor(index, Color(int(r), int(g), int(b)))
            else:
                self.pixels[index] = (int(r), int(g), int(b))

    def show(self):
        """Überträgt die Farbdaten an die LEDs."""
        if HAS_HARDWARE:
            self.strip.show()

    def fill(self, color: tuple):
        """Füllt das gesamte Band mit einer Farbe."""
        for i in range(self.num_leds):
            self.set_pixel(i, color)
        self.show()

    def clear(self):
        """Schaltet alle LEDs aus."""
        self.fill((0, 0, 0))