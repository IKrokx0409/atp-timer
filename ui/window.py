from PyQt6.QtCore    import Qt, QTimer
from PyQt6.QtGui     import QShortcut, QKeySequence, QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMenu

from .solar_system import SolarSystemScene, SolarSystemView
from core.timer    import PomodoroTimer, TimerState


class MainWindow(QWidget):

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self._current_panel = None   # currently open floating panel (or None)
        self.timer = PomodoroTimer(config)
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

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    # ── signals ───────────────────────────────────────────────────────

    def _connect_signals(self) -> None:
        self.scene.body_clicked.connect(self._on_body_clicked)

        # Timer → scene
        self.timer.tick.connect(self._on_timer_tick)
        self.timer.evolution.connect(self.scene.set_evolution)
        self.timer.state_changed.connect(self._on_state_changed)
        self.timer.session_ended.connect(self._on_session_ended)

        # Right-click context menu
        self.view.context_menu_requested.connect(self._show_context_menu)

        # Keyboard shortcuts (work when window or any child has focus)
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, self._toggle_timer)
        QShortcut(QKeySequence(Qt.Key.Key_R),     self, self.timer.reset)

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
        if name in ("Ash Twin", "Ember Twin"):
            from .panels.ash_twin_panel import AshTwinPanel
            return AshTwinPanel(self)
        if name == "Giant's Deep":
            from .panels.giants_deep_panel import GiantsDeepPanel
            return GiantsDeepPanel(self)
        if name == "Brittle Hollow":
            from .panels.brittle_hollow_panel import BrittleHollowPanel
            return BrittleHollowPanel(self)
        return None

    # ── timer controls ────────────────────────────────────────────────

    def _toggle_timer(self) -> None:
        state = self.timer.state
        if state == TimerState.IDLE:
            self.timer.start()
        elif state == TimerState.PAUSED:
            self.timer.resume()
        else:
            self.timer.pause()

    def _on_timer_tick(self, remaining: float) -> None:
        self.scene.set_remaining(remaining)

    def _on_state_changed(self, state: str) -> None:
        self.scene.set_timer_state(state)
        running = state in ("focus", "short_break", "long_break")
        self.scene.set_clickable(not running)
        if running and self._current_panel is not None:
            self._current_panel.close()
            self._current_panel = None

    def _on_session_ended(self) -> None:
        self.scene.trigger_supernova()
        if self.config.get("end_behavior") == "restart":
            QTimer.singleShot(2000, self.timer.start)

    def _show_context_menu(self) -> None:
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #160a2a;
                color: #c8b4ff;
                border: 1px solid #3d2a6e;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item { padding: 6px 20px; border-radius: 4px; }
            QMenu::item:selected { background-color: #3d2a6e; }
            QMenu::separator { height: 1px; background: #3d2a6e; margin: 4px 8px; }
        """)

        state = self.timer.state
        if state == TimerState.IDLE:
            menu.addAction("Start",  self.timer.start)
        elif state == TimerState.PAUSED:
            menu.addAction("Resume", self.timer.resume)
            menu.addAction("Reset",  self.timer.reset)
        else:
            menu.addAction("Pause",  self.timer.pause)
            menu.addAction("Reset",  self.timer.reset)

        menu.addSeparator()
        menu.addAction("Quit", QApplication.quit)
        menu.exec(QCursor.pos())

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
