from abc import ABC, abstractmethod

class Effect(ABC):
    def __init__(self, name: str):
        self.name = name  # Name des Presets

    @abstractmethod
    def update(self, strip):
        """
        Wird in jedem Frame aufgerufen.
        Berechnet die Farben und setzt sie im Strip/Simulator.
        """
        pass