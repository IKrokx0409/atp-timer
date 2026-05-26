from PyQt6.QtCore    import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from .solar_system import SolarSystemScene, SolarSystemView


class MainWindow(QWidget):

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self._setup_window()
        self._setup_ui()

    # ── window flags & size ───────────────────────────────────────────

    def _setup_window(self) -> None:
        flags = Qt.WindowType.FramelessWindowHint
        if self.config.get("always_on_top", True):
            flags |= Qt.WindowType.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        # Solid dark background — WSLg does not reliably composite transparency.
        # The "space" look comes from the scene's drawBackground dark circle.
        self.setStyleSheet("background-color: #000000;")

        size = self.config.get("window_size", 700)
        self.resize(size, size)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("ATP Timer — Outer Wilds Loop")

    # ── layout ────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scene = SolarSystemScene()
        self.view  = SolarSystemView(self.scene)
        layout.addWidget(self.view)

    # ── keep window square on manual resize ───────────────────────────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        side = min(self.width(), self.height())
        if self.width() != side or self.height() != side:
            self.resize(side, side)
