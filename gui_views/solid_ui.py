import tkinter as tk
from tkinter import ttk, colorchooser

class SolidUI:
    PRESET_COLORS = [
        ("Rot", (255, 0, 0)), ("Grün", (0, 255, 0)), ("Blau", (0, 0, 255)),
        ("Gelb", (255, 255, 0)), ("Cyan", (0, 255, 255)), ("Magenta", (255, 0, 255)),
        ("Orange", (255, 128, 0)), ("Lila", (128, 0, 255)), ("Warmweiß", (255, 200, 120)),
        ("Kaltweiß", (200, 220, 255))
    ]

    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Single Color Einstellungen ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Color Picker Button
        btn_color = ttk.Button(self.frame, text="🎨 Farbe wählen (Color Picker)", command=self._choose_color)
        btn_color.pack(fill=tk.X, pady=5)

        # 10 Presets
        ttk.Label(self.frame, text="Preset-Farben:").pack(anchor=tk.W, pady=(10, 2))
        preset_frame = ttk.Frame(self.frame)
        preset_frame.pack(fill=tk.X, pady=5)

        for i, (name, rgb) in enumerate(self.PRESET_COLORS):
            hex_col = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            btn = tk.Button(preset_frame, bg=hex_col, width=3, relief="flat",
                            command=lambda c=rgb: self._set_color(c))
            btn.grid(row=i // 5, column=i % 5, padx=2, pady=2)

    def _choose_color(self):
        color = colorchooser.askcolor(title="Wähle eine Farbe")
        if color[0]:
            self._set_color([int(c) for c in color[0]])

    def _set_color(self, rgb):
        self.effect.r, self.effect.g, self.effect.b = rgb