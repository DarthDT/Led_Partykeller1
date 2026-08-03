# hardware/combined.py

class CombinedLEDStrip:
    def __init__(self, *strips):
        """
        Nimmt beliebig viele Strip-Objekte entgegen (z. B. Simulator + Hardware)
        und spiegelt alle Befehle an alle enthaltenen Strips.
        """
        self.strips = list(strips)
        # Nimm die LED-Anzahl vom ersten Strip als Referenz
        self.num_leds = strips[0].num_leds if strips else 0

    def _parse_color(self, args, kwargs):
        """Hilfsfunktion: Wandelt flexible Argumente in ein (r, g, b) Tuple um."""
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:
            return (int(args[0]), int(args[1]), int(args[2]))
        elif 'color' in kwargs:
            return kwargs['color']
        return (0, 0, 0)

    def set_pixel(self, index: int, *args, **kwargs):
        """
        Setzt einen Pixel.
        Akzeptiert sowohl set_pixel(i, (r, g, b)) als auch set_pixel(i, r, g, b).
        """
        color = self._parse_color(args, kwargs)
        for strip in self.strips:
            try:
                strip.set_pixel(index, color)
            except TypeError:
                # Falls ein Unter-Strip set_pixel(index, r, g, b) erwartet
                if isinstance(color, (tuple, list)) and len(color) == 3:
                    strip.set_pixel(index, color[0], color[1], color[2])

    def set_all(self, *args, **kwargs):
        """
        Setzt alle LEDs auf eine bestimmte Farbe.
        Akzeptiert sowohl set_all((r, g, b)) als auch set_all(r, g, b).
        """
        color = self._parse_color(args, kwargs)

        for strip in self.strips:
            if hasattr(strip, "set_all"):
                try:
                    strip.set_all(*args, **kwargs)
                except TypeError:
                    strip.set_all(color)
            elif hasattr(strip, "fill"):
                try:
                    strip.fill(color)
                except TypeError:
                    strip.fill(*args)
            else:
                for i in range(self.num_leds):
                    strip.set_pixel(i, color)

    def fill(self, *args, **kwargs):
        """Füllt alle registrierten Strips mit einer Farbe."""
        self.set_all(*args, **kwargs)

    def show(self):
        """Überträgt die Daten auf alle registrierten Strips."""
        for strip in self.strips:
            strip.show()

    def clear(self):
        """Schaltet alle registrierten Strips aus."""
        for strip in self.strips:
            strip.clear()