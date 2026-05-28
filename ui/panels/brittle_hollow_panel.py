from .base_panel import BasePanel


class BrittleHollowPanel(BasePanel):
    """Brittle Hollow — short and long break durations."""

    def __init__(self, main_window) -> None:
        super().__init__("Brittle Hollow", parent=None)
        self._main = main_window
        self._build_content()
        self.adjustSize()

    def _build_content(self) -> None:
        cfg = self._main.config
        self._add_slider_row(
            "Short Break",
            lo=1, hi=15, step=1,
            value=cfg["short_break_minutes"], unit="min",
            on_change=lambda v: self._main.config.__setitem__("short_break_minutes", v),
        )
        self._add_slider_row(
            "Long Break",
            lo=5, hi=30, step=1,
            value=cfg["long_break_minutes"], unit="min",
            on_change=lambda v: self._main.config.__setitem__("long_break_minutes", v),
        )
