import tkinter as tk
from tkinter import ttk, colorchooser


class GradientUI:
    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Farbverlauf / Regenbogen Einstellungen ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 1. Modus-Wahl (Regenbogen vs. Custom)
        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.mode_var = tk.StringVar(value="rainbow" if self.effect.is_rainbow else "custom")

        rb_rainbow = ttk.Radiobutton(mode_frame, text="🌈 Regenbogen-Preset", value="rainbow",
                                     variable=self.mode_var, command=self._on_mode_change)
        rb_rainbow.pack(side=tk.LEFT, padx=(0, 15))

        rb_custom = ttk.Radiobutton(mode_frame, text="🎨 Eigene Farben (2 - 4)", value="custom",
                                    variable=self.mode_var, command=self._on_mode_change)
        rb_custom.pack(side=tk.LEFT)

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # 2. Container für Farbfelder
        self.colors_frame = ttk.Frame(self.frame)
        self.colors_frame.pack(fill=tk.X, pady=5)

        self._render_color_controls()

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # 3. Regler: Geschwindigkeit & Wiederholungen
        ttk.Label(self.frame, text="Geschwindigkeit:").pack(anchor=tk.W)
        s_speed = ttk.Scale(self.frame, from_=0.0, to=0.2, value=self.effect.speed,
                            command=lambda v: setattr(self.effect, 'speed', float(v)))
        s_speed.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self.frame, text="Muster-Wiederholungen auf dem Strip:").pack(anchor=tk.W)
        s_repeat = ttk.Scale(self.frame, from_=0.5, to=5.0, value=self.effect.repeat,
                             command=lambda v: setattr(self.effect, 'repeat', float(v)))
        s_repeat.pack(fill=tk.X, pady=(0, 5))

    def _on_mode_change(self):
        if self.mode_var.get() == "rainbow":
            self.effect.set_rainbow_mode(True)
        else:
            # Bei Wechsel zu Custom mit 2 Standardfarben starten, falls vorher Regenbogen war
            if len(self.effect.colors) > 4:
                self.effect.set_custom_colors([(255, 0, 0), (0, 0, 255)])
            else:
                self.effect.is_rainbow = False
        self._render_color_controls()

    def _render_color_controls(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        if self.effect.is_rainbow:
            ttk.Label(self.colors_frame, text="Regenbogen-Modus aktiv (7 Spektralfarben)",
                      font=("Arial", 9, "italic")).pack(anchor=tk.W)
        else:
            # Color-Buttons für 2 bis 4 Farben rendern
            btn_container = ttk.Frame(self.colors_frame)
            btn_container.pack(fill=tk.X)

            for idx, rgb in enumerate(self.effect.colors):
                r, g, b = rgb
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                text_color = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

                btn = tk.Button(
                    btn_container, text=f"🎨 Farbe {idx + 1}", bg=hex_col, fg=text_color,
                    font=("Arial", 9, "bold"), relief="raised", padx=6, pady=4,
                    command=lambda i=idx: self._choose_color(i)
                )
                btn.grid(row=0, column=idx, padx=3)

            # Plus/Minus Buttons für Farbe hinzufügen/entfernen
            ctrl_frame = ttk.Frame(self.colors_frame)
            ctrl_frame.pack(fill=tk.X, pady=(5, 0))

            if len(self.effect.colors) < 4:
                ttk.Button(ctrl_frame, text="+ Farbe hinzufügen", command=self._add_color).pack(side=tk.LEFT, padx=2)
            if len(self.effect.colors) > 2:
                ttk.Button(ctrl_frame, text="- Farbe entfernen", command=self._remove_color).pack(side=tk.LEFT, padx=2)

    def _choose_color(self, idx):
        color = colorchooser.askcolor(title=f"Farbe {idx + 1} wählen")
        if color[0]:
            rgb = tuple(int(c) for c in color[0])
            current = list(self.effect.colors)
            current[idx] = rgb
            self.effect.set_custom_colors(current)
            self._render_color_controls()

    def _add_color(self):
        current = list(self.effect.colors)
        if len(current) < 4:
            current.append((0, 255, 0))  # Grün als Standard beim Hinzufügen
            self.effect.set_custom_colors(current)
            self._render_color_controls()

    def _remove_color(self):
        current = list(self.effect.colors)
        if len(current) > 2:
            current.pop()
            self.effect.set_custom_colors(current)
            self._render_color_controls()