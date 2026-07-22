import tkinter as tk
from tkinter import ttk, colorchooser


class MusicStrobeUI:
    """GUI-Panel zur Steuerung des Beat-Sparkle Strobo Effekts."""

    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Beat Sparkle / Strobo Glitzern ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 1. Sensitivity / Empfindlichkeit
        ttk.Label(self.frame, text="Empfindlichkeit (Beat Trigger):").pack(anchor=tk.W)
        s_sens = ttk.Scale(
            self.frame, from_=0.5, to=5.0, value=self.effect.sensitivity,
            command=lambda v: setattr(self.effect, 'sensitivity', float(v))
        )
        s_sens.pack(fill=tk.X, pady=(0, 8))

        # 2. Ausfadedauer / Decay Speed
        ttk.Label(self.frame, text="Blitz-Dauer / Ausfaden (Decay):").pack(anchor=tk.W)
        s_decay = ttk.Scale(
            self.frame, from_=0.50, to=0.95, value=self.effect.decay,
            command=lambda v: setattr(self.effect, 'decay', float(v))
        )
        s_decay.pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # 3. Weißes Strobo-Glitzern An/Aus
        self.white_var = tk.BooleanVar(value=self.effect.enable_white_strobe)
        chk_white = ttk.Checkbutton(
            self.frame, text="⚡ Weißes Stroboskop-Glitzern erlauben",
            variable=self.white_var, command=self._on_white_toggle
        )
        chk_white.pack(anchor=tk.W, pady=(5, 2))

        # 3b. Dezentes Nachglitzern an den Rändern
        self.afterglow_var = tk.BooleanVar(value=getattr(self.effect, 'enable_afterglow', True))
        chk_afterglow = ttk.Checkbutton(
            self.frame, text="✨ Dezentes Nachglitzern an den Rändern",
            variable=self.afterglow_var, command=self._on_afterglow_toggle
        )
        chk_afterglow.pack(anchor=tk.W, pady=(0, 10))

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)


        # 4. Farbauswahl (2 bis 4 Farben)
        ttk.Label(self.frame, text="Farbige Glitzerblitze (2 bis 4 Farben):", font=("Arial", 9, "bold")).pack(
            anchor=tk.W, pady=(5, 2))

        self.colors_frame = ttk.Frame(self.frame)
        self.colors_frame.pack(fill=tk.X, pady=5)

        self._render_colors()

    def _on_white_toggle(self):
        self.effect.enable_white_strobe = self.white_var.get()

    def _on_afterglow_toggle(self):
        self.effect.enable_afterglow = self.afterglow_var.get()

    def _render_colors(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        btn_box = ttk.Frame(self.colors_frame)
        btn_box.pack(fill=tk.X, pady=5)

        for idx, rgb in enumerate(self.effect.colors):
            r, g, b = rgb
            hex_col = f"#{r:02x}{g:02x}{b:02x}"
            txt_col = "#ffffff" if (r * 0.299 + g * 0.587 + b * 0.114) < 128 else "#000000"

            btn = tk.Button(
                btn_box, text=f"Farbe {idx + 1}", bg=hex_col, fg=txt_col,
                font=("Arial", 9, "bold"), command=lambda i=idx: self._choose_color(i),
                padx=6, pady=3
            )
            btn.grid(row=0, column=idx, padx=3)

        ctrl_frame = ttk.Frame(self.colors_frame)
        ctrl_frame.pack(fill=tk.X, pady=(5, 0))

        if len(self.effect.colors) < 4:
            ttk.Button(ctrl_frame, text="+ Farbe hinzufügen", command=self._add_color).pack(side=tk.LEFT, padx=2)
        if len(self.effect.colors) > 2:  # Mindestens 2 Farben
            ttk.Button(ctrl_frame, text="- Farbe entfernen", command=self._remove_color).pack(side=tk.LEFT, padx=2)

    def _choose_color(self, idx):
        color = colorchooser.askcolor(title=f"Glitzer-Farbe {idx + 1} wählen")
        if color[0]:
            current = list(self.effect.colors)
            current[idx] = tuple(int(c) for c in color[0])
            self.effect.colors = current
            self._render_colors()

    def _add_color(self):
        current = list(self.effect.colors)
        if len(current) < 4:
            current.append((255, 255, 0))  # Standardmäßig Gelb hinzufügen
            self.effect.colors = current
            self._render_colors()

    def _remove_color(self):
        current = list(self.effect.colors)
        if len(current) > 2:
            current.pop()
            self.effect.colors = current
            self._render_colors()