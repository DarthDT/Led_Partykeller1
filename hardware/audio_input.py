import sounddevice as sd
import numpy as np


class AudioAnalyzer:
    def __init__(self, rate=44100, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.volume = 0.0
        self.stream = None

    def _find_loopback_device(self):
        """Sucht automatisch nach dem System-Audioausgang (Loopback/Stereomix)."""
        devices = sd.query_devices()

        # Typische Namen für Audio-Loopbacks unter Windows, Linux (Raspberry Pi) und Mac
        keywords = ["loopback", "stereo mix", "stereomix", "what u hear", "monitor", "waveout"]

        print("\n--- Verfuogbare Audio-Eingänge ---")
        for idx, dev in enumerate(devices):
            # Wir suchen nur unter Eingabegeräten (max_input_channels > 0)
            if dev['max_input_channels'] > 0:
                name_lower = dev['name'].lower()
                print(f"[{idx}] {dev['name']}")

                # Prüfen, ob der Name eines unserer Schlüsselwörter enthält
                for kw in keywords:
                    if kw in name_lower:
                        print(f"--> System-Sound Output gefunden: [{idx}] {dev['name']}\n")
                        return idx

        # Falls kein Loopback-Gerät gefunden wurde, Standard-Eingang nutzen
        default_dev = sd.default.device[0]
        print(f"--> Kein Loopback gefunden. Nutze Standard-Eingang [{default_dev}]\n")
        return default_dev

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass  # Eventuelle Audio-Buffer-Overflows ignorieren
        # RMS (Effektivwert der Lautstärke) berechnen
        rms = np.sqrt(np.mean(indata ** 2))
        self.volume = float(rms)

    def start(self):
        try:
            device_id = self._find_loopback_device()

            self.stream = sd.InputStream(
                device=device_id,
                samplerate=self.rate,
                blocksize=self.chunk,
                channels=1,
                callback=self._audio_callback
            )
            self.stream.start()
            print("Audio-Analyzer erfolgreich auf System-Sound gestartet!")
        except Exception as e:
            print(f"Fehler beim Starten des Audio-Streams: {e}")

    def get_volume(self):
        """Gibt die Lautstärke normiert von 0.0 bis 1.0 zurück."""
        normalized = self.volume * 10.0  # Anpassen je nach System-Pegel
        return max(0.0, min(1.0, normalized))

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()