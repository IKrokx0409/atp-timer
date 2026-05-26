from PyQt6.QtCore    import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication

from .solar_system import SolarSystemScene, SolarSystemView


class MainWindow(QWidget):

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self._current_panel = None   # currently open floating panel (or None)
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        self._position_bottom_right()

    # ── window flags & size ───────────────────────────────────────────

    def _setup_window(self) -> None:
        flags = Qt.WindowType.FramelessWindowHint
        if self.config.get("always_on_top", True):
            flags |= Qt.WindowType.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        # True per-pixel transparency via Windows DWM.
        # The scene's drawBackground paints the dark space circle;
        # everything outside it stays fully transparent.
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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

    # ── signals ───────────────────────────────────────────────────────

    def _connect_signals(self) -> None:
        self.scene.body_clicked.connect(self._on_body_clicked)

    def _on_body_clicked(self, name: str) -> None:
        # Close any already-open panel first
        if self._current_panel is not None:
            self._current_panel.close()
            self._current_panel = None

        panel = self._make_panel(name)
        if panel is None:
            return

        self._current_panel = panel
        panel.closed.connect(self._on_panel_closed)
        self._position_panel(panel)
        panel.show()
        panel.raise_()

    def _on_panel_closed(self) -> None:
        self._current_panel = None

    def _make_panel(self, name: str):
        """Return a panel widget for the given body name, or None if not implemented."""
        if name == "Timber Hearth":
            from .panels.timber_hearth_panel import TimberHearthPanel
            return TimberHearthPanel(self)
        # Other panels: placeholder — add here as they are implemented
        return None

    # ── panel placement ───────────────────────────────────────────────

    def _position_panel(self, panel: QWidget) -> None:
        """Place the panel just to the left of the main window, vertically centred."""
        panel.adjustSize()
        geo  = self.frameGeometry()
        px   = geo.left() - panel.width() - 12
        py   = geo.top() + (geo.height() - panel.height()) // 2
        # Keep on screen
        screen = QApplication.primaryScreen().availableGeometry()
        if px < screen.left():
            px = geo.right() + 12
        py = max(screen.top(), min(py, screen.bottom() - panel.height()))
        panel.move(px, py)

    # ── initial window placement ──────────────────────────────────────

    def _position_bottom_right(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        margin = 16
        x = screen.right()  - self.width()  - margin
        y = screen.bottom() - self.height() - margin
        self.move(x, y)

    # ── live resize helper (called by TimberHearthPanel) ─────────────

    def set_window_size(self, size: int) -> None:
        self.resize(size, size)
        self.config["window_size"] = size
        self._position_bottom_right()   # re-anchor to corner after resize

    # ── keep window square on manual resize ───────────────────────────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        side = min(self.width(), self.height())
        if self.width() != side or self.height() != side:
            self.resize(side, side)
