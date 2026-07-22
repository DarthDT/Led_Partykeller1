class PresetManager:
    def __init__(self):
        self.presets = {}
        self.active_key = None

    def add_preset(self, key: str, effect_object):
        """Fügt ein neues Preset unter einem eindeutigen Namen (Key) hinzu."""
        self.presets[key] = effect_object
        if self.active_key is None:
            self.active_key = key

    def select_preset(self, key: str) -> bool:
        """Aktiviert ein Preset über seinen Namen."""
        if key in self.presets:
            self.active_key = key
            print(f"Preset gewechselt zu: '{self.presets[key].name}' ({key})")
            return True
        else:
            print(f"Fehler: Preset '{key}' nicht gefunden!")
            return False

    def get_active_effect(self):
        """Gibt das aktuell aktive Effekt-Objekt zurück."""
        if self.active_key:
            return self.presets[self.active_key]
        return None

    def get_available_presets(self):
        """Liefert eine Liste aller verfügbaren Preset-Namen."""
        return list(self.presets.keys())