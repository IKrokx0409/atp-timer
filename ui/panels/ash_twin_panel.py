from .base_panel import BasePanel


class AshTwinPanel(BasePanel):
    """Hourglass Twins — focus duration setting (5–60 min)."""

    def __init__(self, main_window) -> None:
        super().__init__("Hourglass Twins", parent=None)
        self._main = main_window
        self._build_content()
        self.adjustSize()

    def _build_content(self) -> None:
        current = self._main.config["loop_duration_minutes"]
        self._add_slider_row(
            "Focus Duration",
            lo=5, hi=60, step=1,
            value=current, unit="min",
            on_change=self._on_change,
        )

    def _on_change(self, value: int) -> None:
        self._main.config["loop_duration_minutes"] = value
