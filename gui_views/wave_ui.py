import tkinter as tk
from tkinter import ttk, colorchooser


class WaveUI:
    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Waber-Effekt Einstellungen ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 1. Softness Slider (Flächengröße)
        ttk.Label(self.frame, text="Flächengröße (Scale):").pack(anchor=tk.W)
        s_softness = ttk.Scale(self.frame, from_=0.1, to=0.005, value=self.effect.scale,
                               command=lambda v: setattr(self.effect, 'scale', float(v)))
        s_softness.pack(fill=tk.X, pady=(0, 8))

        # 2. Kontrast / Übergangs-Stärke Slider (NEU! 💥)
        ttk.Label(self.frame, text="Farb-Klarheit / Kontrast (Übergangsstärke):", font=("Arial", 9, "bold")).pack(
            anchor=tk.W)
        s_contrast = ttk.Scale(self.frame, from_=1.0, to=5.0, value=self.effect.contrast,
                               command=lambda v: setattr(self.effect, 'contrast', float(v)))
        s_contrast.pack(fill=tk.X, pady=(0, 8))

        # 3. Geschwindigkeit Slider
        ttk.Label(self.frame, text="Geschwindigkeit:").pack(anchor=tk.W)
        s_speed = ttk.Scale(self.frame, from_=0.001, to=0.1, value=self.effect.speed,
                            command=lambda v: setattr(self.effect, 'speed', float(v)))
        s_speed.pack(fill=tk.X, pady=(0, 10))

        # 4. Farbauswahl & Buttons
        ttk.Label(self.frame, text="Farben anpassen (2 bis 3 Farben):", font=("Arial", 9, "bold")).pack(anchor=tk.W,
                                                                                                        pady=(5, 5))

        self.colors_frame = ttk.Frame(self.frame)
        self.colors_frame.pack(fill=tk.X, pady=5)

        self._render_color_buttons()

    def _render_color_buttons(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        for idx, rgb in enumerate(self.effect.colors):
            r, g, b = rgb
            hex_col = f"#{r:02x}{g:02x}{b:02x}"
            text_color = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

            btn = tk.Button(
                self.colors_frame, text=f"🎨 Farbe {idx + 1}", bg=hex_col, fg=text_color,
                font=("Arial", 9, "bold"), relief="raised", padx=6, pady=4,
                command=lambda i=idx: self._choose_color(i)
            )
            btn.grid(row=0, column=idx, padx=4)

        control_btn_frame = ttk.Frame(self.colors_frame)
        control_btn_frame.grid(row=0, column=len(self.effect.colors), padx=10)

        if len(self.effect.colors) == 2:
            btn_add = ttk.Button(control_btn_frame, text="+ 3. Farbe", command=self._add_color)
            btn_add.pack()
        elif len(self.effect.colors) == 3:
            btn_remove = ttk.Button(control_btn_frame, text="- 3. Farbe löschen", command=self._remove_color)
            btn_remove.pack()

    def _choose_color(self, idx):
        color = colorchooser.askcolor(title=f"Farbe {idx + 1} wählen")
        if color[0]:
            rgb = tuple(int(c) for c in color[0])
            current_colors = list(self.effect.colors)
            current_colors[idx] = rgb
            self.effect.set_colors(current_colors)
            self._render_color_buttons()

    def _add_color(self):
        current_colors = list(self.effect.colors)
        if len(current_colors) < 3:
            current_colors.append((128, 0, 255))
            self.effect.set_colors(current_colors)
            self._render_color_buttons()

    def _remove_color(self):
        current_colors = list(self.effect.colors)
        if len(current_colors) > 2:
            current_colors.pop()
            self.effect.set_colors(current_colors)
            self._render_color_buttons()