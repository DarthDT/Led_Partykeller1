import tkinter as tk
from tkinter import ttk, colorchooser


class MusicRunnerUI:
    """GUI-Panel zur Steuerung des Music Runner Effekts."""

    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Music Runner Steuerung ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 1. Musik-Reaktion An/Aus
        self.music_var = tk.BooleanVar(value=self.effect.enable_music)
        chk_music = ttk.Checkbutton(
            self.frame, text="🎵 Musikreaktion aktivieren (Beat Flash)",
            variable=self.music_var, command=self._on_music_toggle
        )
        chk_music.pack(anchor=tk.W, pady=(0, 8))

        # 2. Grundhelligkeit & Fadeout Regler
        sliders_frame = ttk.Frame(self.frame)
        sliders_frame.pack(fill=tk.X, pady=5)

        ttk.Label(sliders_frame, text="Grundhelligkeit (10% - 90%):").grid(row=0, column=0, sticky=tk.W)
        s_bright = ttk.Scale(
            sliders_frame, from_=0.10, to=0.90, value=self.effect.base_brightness,
            command=lambda v: setattr(self.effect, 'base_brightness', float(v))
        )
        s_bright.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(sliders_frame, text="Fadeout Dauer (1 - 10 Sek):").grid(row=1, column=0, sticky=tk.W)
        s_fade = ttk.Scale(
            sliders_frame, from_=1.0, to=10.0, value=self.effect.fadeout_sec,
            command=lambda v: setattr(self.effect, 'fadeout_sec', float(v))
        )
        s_fade.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(sliders_frame, text="Geschwindigkeit:").grid(row=2, column=0, sticky=tk.W)
        s_speed = ttk.Scale(
            sliders_frame, from_=0.5, to=5.0, value=self.effect.speed,
            command=lambda v: setattr(self.effect, 'speed', float(v))
        )
        s_speed.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)

        sliders_frame.columnconfigure(1, weight=1)

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=8)

        # 3. Laufrichtung
        ttk.Label(self.frame, text="Laufrichtung:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.dir_var = tk.StringVar(value=self.effect.direction)

        dir_frame = ttk.Frame(self.frame)
        dir_frame.pack(fill=tk.X, pady=4)

        directions = [
            ("➡️ Links → Rechts", "left_to_right"),
            ("⬅️ Rechts → Links", "right_to_left"),
            ("➡️⬅️ Außen → Mitte", "edges_to_center"),
            ("⬅️➡️ Mitte → Außen", "center_to_edges")
        ]

        for text, val in directions:
            rb = ttk.Radiobutton(
                dir_frame, text=text, value=val,
                variable=self.dir_var, command=self._on_direction_change
            )
            rb.pack(anchor=tk.W)

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=8)

        # 4. Farbmodus (Solid, Gradient, Rainbow)
        ttk.Label(self.frame, text="Farbe / Animation:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.color_mode_var = tk.StringVar(value=self.effect.color_mode)

        mode_frame = ttk.Frame(self.frame)
        mode_frame.pack(fill=tk.X, pady=4)

        ttk.Radiobutton(mode_frame, text="Einfarbig", value="solid", variable=self.color_mode_var,
                        command=self._on_color_mode_change).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="Gradient (2-4 Farben)", value="custom_gradient", variable=self.color_mode_var,
                        command=self._on_color_mode_change).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="🌈 Regenbogen", value="rainbow", variable=self.color_mode_var,
                        command=self._on_color_mode_change).pack(side=tk.LEFT)

        # Container für Farbfelder
        self.colors_box = ttk.Frame(self.frame)
        self.colors_box.pack(fill=tk.X, pady=5)

        self._render_color_controls()

    def _on_music_toggle(self):
        self.effect.enable_music = self.music_var.get()

    def _on_direction_change(self):
        self.effect.direction = self.dir_var.get()

    def _on_color_mode_change(self):
        self.effect.color_mode = self.color_mode_var.get()
        self._render_color_controls()

    def _render_color_controls(self):
        for widget in self.colors_box.winfo_children():
            widget.destroy()

        mode = self.effect.color_mode

        if mode == "solid":
            r, g, b = self.effect.solid_color
            hex_col = f"#{r:02x}{g:02x}{b:02x}"
            btn = tk.Button(
                self.colors_box, text="Hauptfarbe wählen", bg=hex_col,
                command=self._choose_solid_color, padx=10, pady=3
            )
            btn.pack(anchor=tk.W, pady=5)

        elif mode == "custom_gradient":
            btn_box = ttk.Frame(self.colors_box)
            btn_box.pack(fill=tk.X, pady=2)

            for idx, rgb in enumerate(self.effect.custom_colors):
                r, g, b = rgb
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                txt_col = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

                btn = tk.Button(
                    btn_box, text=f"Farbe {idx + 1}", bg=hex_col, fg=txt_col,
                    font=("Arial", 9, "bold"), command=lambda i=idx: self._choose_gradient_color(i),
                    padx=6, pady=3
                )
                btn.grid(row=0, column=idx, padx=3)

            ctrl_frame = ttk.Frame(self.colors_box)
            ctrl_frame.pack(fill=tk.X, pady=(5, 0))

            if len(self.effect.custom_colors) < 4:
                ttk.Button(ctrl_frame, text="+ Farbe", command=self._add_gradient_color).pack(side=tk.LEFT, padx=2)
            if len(self.effect.custom_colors) > 2:
                ttk.Button(ctrl_frame, text="- Farbe", command=self._remove_gradient_color).pack(side=tk.LEFT, padx=2)

    def _choose_solid_color(self):
        color = colorchooser.askcolor(title="Runner-Farbe wählen")
        if color[0]:
            self.effect.solid_color = tuple(int(c) for c in color[0])
            self._render_color_controls()

    def _choose_gradient_color(self, idx):
        color = colorchooser.askcolor(title=f"Gradient-Farbe {idx + 1} wählen")
        if color[0]:
            current = list(self.effect.custom_colors)
            current[idx] = tuple(int(c) for c in color[0])
            self.effect.custom_colors = current
            self._render_color_controls()

    def _add_gradient_color(self):
        current = list(self.effect.custom_colors)
        if len(current) < 4:
            current.append((0, 255, 255))
            self.effect.custom_colors = current
            self._render_color_controls()

    def _remove_gradient_color(self):
        current = list(self.effect.custom_colors)
        if len(current) > 2:
            current.pop()
            self.effect.custom_colors = current
            self._render_color_controls()