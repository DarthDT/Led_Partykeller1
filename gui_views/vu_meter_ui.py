import tkinter as tk
from tkinter import ttk, colorchooser


class VuMeterUI:
    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Sound VU-Meter (Mitte → Außen) ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 1. Empfindlichkeit / Gain Slider
        ttk.Label(self.frame, text="Audio Empfindlichkeit (Gain):").pack(anchor=tk.W)
        s_gain = ttk.Scale(self.frame, from_=0.5, to=5.0, value=self.effect.sensitivity,
                           command=lambda v: setattr(self.effect, 'sensitivity', float(v)))
        s_gain.pack(fill=tk.X, pady=(0, 10))

        # 2. Peak Color Picker
        ttk.Label(self.frame, text="Peak Marker (Spitzenwert):", font=("Arial", 9, "bold")).pack(anchor=tk.W,
                                                                                                 pady=(5, 2))
        self.btn_peak = tk.Button(self.frame, text="🎨 Peak Farbe wählen", font=("Arial", 9, "bold"),
                                  command=self._choose_peak_color, relief="raised", padx=6, pady=3)
        self.btn_peak.pack(anchor=tk.W, pady=(0, 10))
        self._update_peak_btn_style()

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # 3. Farb-Modus Umschalter (Solid vs. Gradient)
        ttk.Label(self.frame, text="Ausschlag Farb-Modus:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(5, 2))

        self.mode_var = tk.StringVar(value=self.effect.color_mode)
        rb_solid = ttk.Radiobutton(self.frame, text="Solid (Einfarbig)", value="solid",
                                   variable=self.mode_var, command=self._on_mode_change)
        rb_solid.pack(anchor=tk.W)

        rb_grad = ttk.Radiobutton(self.frame, text="Gradient (Farbverlauf)", value="gradient",
                                  variable=self.mode_var, command=self._on_mode_change)
        rb_grad.pack(anchor=tk.W, pady=(0, 5))

        # Dynamic Color Frame
        self.colors_frame = ttk.Frame(self.frame)
        self.colors_frame.pack(fill=tk.X, pady=5)
        self._render_color_options()

    def _on_mode_change(self):
        self.effect.color_mode = self.mode_var.get()
        self._render_color_options()

    def _update_peak_btn_style(self):
        r, g, b = self.effect.peak_color
        hex_col = f"#{r:02x}{g:02x}{b:02x}"
        txt_col = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"
        self.btn_peak.config(bg=hex_col, fg=txt_col)

    def _choose_peak_color(self):
        color = colorchooser.askcolor(title="Peak Farbe wählen")
        if color[0]:
            self.effect.peak_color = tuple(int(c) for c in color[0])
            self._update_peak_btn_style()

    def _render_color_options(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        if self.effect.color_mode == "solid":
            r, g, b = self.effect.solid_color
            hex_col = f"#{r:02x}{g:02x}{b:02x}"
            txt_col = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

            btn = tk.Button(self.colors_frame, text="🎨 Balken Farbe", bg=hex_col, fg=txt_col,
                            font=("Arial", 9, "bold"), command=self._choose_solid_color, padx=6, pady=3)
            btn.pack(anchor=tk.W)
        else:
            ttk.Label(self.colors_frame, text="Gradient Farben (Mitte → Rand):").pack(anchor=tk.W)
            btn_box = ttk.Frame(self.colors_frame)
            btn_box.pack(fill=tk.X, pady=2)

            for idx, rgb in enumerate(self.effect.gradient_colors):
                r, g, b = rgb
                hex_col = f"#{r:02x}{g:02x}{b:02x}"
                txt_col = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

                btn = tk.Button(btn_box, text=f"Farbe {idx + 1}", bg=hex_col, fg=txt_col,
                                font=("Arial", 8, "bold"), command=lambda i=idx: self._choose_grad_color(i))
                btn.grid(row=0, column=idx, padx=3)

    def _choose_solid_color(self):
        color = colorchooser.askcolor(title="Balken Farbe")
        if color[0]:
            self.effect.solid_color = tuple(int(c) for c in color[0])
            self._render_color_options()

    def _choose_grad_color(self, idx):
        color = colorchooser.askcolor(title=f"Gradient Farbe {idx + 1}")
        if color[0]:
            current = list(self.effect.gradient_colors)
            current[idx] = tuple(int(c) for c in color[0])
            self.effect.gradient_colors = current
            self._render_color_options()