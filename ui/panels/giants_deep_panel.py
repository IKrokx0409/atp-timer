from .base_panel import BasePanel


class GiantsDeepPanel(BasePanel):
    """Giant's Deep — number of Pomodoro cycles (1–8)."""

    def __init__(self, main_window) -> None:
        super().__init__("Giant's Deep", parent=None)
        self._main = main_window
        self._build_content()
        self.adjustSize()

    def _build_content(self) -> None:
        current = self._main.config["cycles"]
        self._add_slider_row(
            "Pomodoro Cycles",
            lo=1, hi=8, step=1,
            value=current, unit="",
            on_change=self._on_change,
        )

    def _on_change(self, value: int) -> None:
        self._main.config["cycles"] = value
