import tkinter as tk
from tkinter import ttk

# UI-Module importieren
from gui_views.solid_ui import SolidUI
from gui_views.chase_ui import ChaseUI
from gui_views.wave_ui import WaveUI
from gui_views.gradient_ui import GradientUI
from gui_views.vu_meter_ui import VuMeterUI
from gui_views.music_strobe_ui import MusicStrobeUI
from gui_views.music_runner_ui import MusicRunnerUI

# Effekte importieren zur Typ-Prüfung
from effects.solid import SolidEffect
from effects.chase import ChaseEffect
from effects.wave import WaveEffect
from effects.gradient import GradientEffect
from effects.vu_meter import VuMeterEffect
from effects.music_strobe import MusicStrobeEffect
from effects.music_runner import MusicRunnerEffect



class ControlPanelGUI:
    def __init__(self, manager):
        self.manager = manager

        self.root = tk.Tk()
        self.root.title("Partykeller LED Controller - Steuerung")
        self.root.geometry("600x450")

        # Zuordnung: Welcher Effekt braucht welches UI-Modul?
        self.ui_map = {
            SolidEffect: SolidUI,
            ChaseEffect: ChaseUI,
            WaveEffect: WaveUI,
            GradientEffect: GradientUI,
            VuMeterEffect: VuMeterUI,
            MusicStrobeEffect: MusicStrobeUI,
            MusicRunnerEffect: MusicRunnerUI,
        }

        self._build_layout()

    def _build_layout(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # LINKS: Effektliste
        left_frame = ttk.LabelFrame(main_frame, text=" Presets / Effekte ", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.effect_listbox = tk.Listbox(left_frame, width=22, font=("Arial", 11))
        self.effect_listbox.pack(fill=tk.BOTH, expand=True)
        self.effect_listbox.bind("<<ListboxSelect>>", self._on_effect_select)

        for key in self.manager.get_available_presets():
            self.effect_listbox.insert(tk.END, key)

        # RECHTS: Parameter Container
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        if self.manager.get_available_presets():
            self.effect_listbox.selection_set(0)
            self._on_effect_select(None)

    def _on_effect_select(self, event):
        selection = self.effect_listbox.curselection()
        if not selection:
            return

        key = self.effect_listbox.get(selection[0])
        self.manager.select_preset(key)
        effect = self.manager.get_active_effect()

        # Rechten Bereich leeren
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Passende UI-Klasse dynamisch laden
        ui_class = self.ui_map.get(type(effect))
        if ui_class:
            ui_class(self.right_frame, effect)

    def update(self):
        self.root.update_idletasks()
        self.root.update()