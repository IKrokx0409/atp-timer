import json
from pathlib import Path

DEFAULTS: dict = {
    "loop_duration_minutes": 22,
    "cycles": 4,
    "short_break_minutes": 5,
    "long_break_minutes": 15,
    "always_on_top": True,
    "window_opacity": 1.0,
    "sound_enabled": True,
    "volume": 0.8,
    "supernova_animation": True,
    "end_behavior": "restart",   # "restart" | "notify" | "quit"
    "window_size": 700,
}


class Config:
    def __init__(self, path: str = "config.json") -> None:
        self._path = Path(path)
        self._data: dict = DEFAULTS.copy()
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                with self._path.open() as f:
                    self._data.update(json.load(f))
            except Exception:
                pass

    def save(self) -> None:
        with self._path.open("w") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value
        self.save()

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value) -> None:
        self.set(key, value)
