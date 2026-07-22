import tkinter as tk
from tkinter import ttk, colorchooser


class ChaseUI:
    def __init__(self, parent_frame, effect):
        self.effect = effect
        self.frame = ttk.LabelFrame(parent_frame, text=" Lauflicht Einstellungen ", padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # --- FARBWAHL BEREICH ---
        ttk.Label(self.frame, text="Farben anpassen (Fade Head → Tail):", font=("Arial", 9, "bold")).pack(anchor=tk.W,
                                                                                                          pady=(0, 5))

        self.colors_frame = ttk.Frame(self.frame)
        self.colors_frame.pack(fill=tk.X, pady=(0, 10))

        self._render_color_buttons()

        ttk.Separator(self.frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # --- SLIDER BEREICH ---
        # 1. Geschwindigkeit
        ttk.Label(self.frame, text="Geschwindigkeit:").pack(anchor=tk.W)
        s_speed = ttk.Scale(self.frame, from_=0.1, to=0.005, value=self.effect.speed,
                            command=lambda v: setattr(self.effect, 'speed', float(v)))
        s_speed.pack(fill=tk.X, pady=(0, 10))

        # 2. Main Length
        ttk.Label(self.frame, text="Kopflänge (Main Length):").pack(anchor=tk.W)
        s_head = ttk.Scale(self.frame, from_=1, to=10, value=self.effect.head_length,
                           command=lambda v: setattr(self.effect, 'head_length', int(float(v))))
        s_head.pack(fill=tk.X, pady=(0, 10))

        # 3. Trail Length
        ttk.Label(self.frame, text="Schweiflänge (Trail Length):").pack(anchor=tk.W)
        s_tail = ttk.Scale(self.frame, from_=0, to=20, value=self.effect.tail_length,
                           command=lambda v: setattr(self.effect, 'tail_length', int(float(v))))
        s_tail.pack(fill=tk.X, pady=(0, 10))

        # 4. Anzahl Chase Objekte
        ttk.Label(self.frame, text="Anzahl Objekte auf Strip:").pack(anchor=tk.W)
        s_num = ttk.Scale(self.frame, from_=1, to=6, value=self.effect.num_objects,
                          command=lambda v: setattr(self.effect, 'num_objects', int(float(v))))
        s_num.pack(fill=tk.X, pady=(0, 10))

    def _render_color_buttons(self):
        # Buttons für Head und Tail erstellen/aktualisieren
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        # Head Color Button
        hr, hg, hb = self.effect.head_color
        hex_head = f"#{hr:02x}{hg:02x}{hb:02x}"
        head_text_col = "#ffffff" if (hr * 0.299 + hg * 0.587 + hb * 0.114) < 128 else "#000000"

        btn_head = tk.Button(
            self.colors_frame, text="🎨 Kopffarbe (Head)", bg=hex_head, fg=head_text_col,
            font=("Arial", 9, "bold"), relief="raised", padx=8, pady=4,
            command=lambda: self._choose_color('head')
        )
        btn_head.grid(row=0, column=0, padx=5)

        # Tail Color Button
        tr, tg, tb = self.effect.tail_color
        hex_tail = f"#{tr:02x}{tg:02x}{tb:02x}"
        tail_text_col = "#ffffff" if (tr * 0.299 + tg * 0.587 + tb * 0.114) < 128 else "#000000"

        btn_tail = tk.Button(
            self.colors_frame, text="🎨 Schweiffarbe (Tail)", bg=hex_tail, fg=tail_text_col,
            font=("Arial", 9, "bold"), relief="raised", padx=8, pady=4,
            command=lambda: self._choose_color('tail')
        )
        btn_tail.grid(row=0, column=1, padx=5)

    def _choose_color(self, target):
        color = colorchooser.askcolor(title=f"Wähle {'Kopffarbe' if target == 'head' else 'Schweiffarbe'}")
        if color[0]:
            rgb = tuple(int(c) for c in color[0])
            if target == 'head':
                self.effect.head_color = rgb
            else:
                self.effect.tail_color = rgb
            self._render_color_buttons()