"""
SolarSystemScene  — QGraphicsScene that owns and animates all bodies.
SolarSystemView   — QGraphicsView wrapper; handles drag-to-move and fitInView.

Scene coordinate space: sun at (0, 0), radius ~330 units.
"""

import time
from PyQt6.QtCore    import Qt, QRectF, QPointF, QTimer, pyqtSignal
from PyQt6.QtGui     import QPainter, QColor, QPen, QBrush, QRadialGradient, QFont
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem

from .bodies.sun            import Sun
from .bodies.sun_station    import SunStation
from .bodies.ash_twin       import HourglassBarycenter, AshTwin, EmberTwin
from .bodies.timber_hearth  import TimberHearth, Attlerock
from .bodies.brittle_hollow import BrittleHollow, HollowsLantern
from .bodies.giants_deep    import GiantsDeep
from .bodies.dark_bramble   import DarkBramble
from .bodies.interloper     import Interloper

SCENE_R = 350   # half-width of the scene bounding box


class SolarSystemScene(QGraphicsScene):

    # Emitted with the body name whenever a planet is clicked
    body_clicked = pyqtSignal(str)

    # Circular orbit guide rings (one per main-body orbit)
    _CIRCULAR_ORBITS = [82, 118, 182, 245, 292, 328]

    def __init__(self) -> None:
        super().__init__()
        self.setSceneRect(-SCENE_R, -SCENE_R, SCENE_R * 2, SCENE_R * 2)
        # Don't let Qt pre-fill the background — drawBackground owns everything
        self.setBackgroundBrush(QBrush(Qt.BrushStyle.NoBrush))

        self._last_t: float | None = None
        self._bodies: list = []

        self._timer_state: str = "idle"
        self._remaining_sec: float = 0.0
        self._evolution_progress: float = 0.0

        self._build()
        self._build_overlay()
        self._start_loop()

    # ── construction ──────────────────────────────────────────────────

    def _build(self) -> None:
        # Instantiate — order matters: parents before children
        self.sun                  = Sun()
        self.sun_station          = SunStation()
        self.hourglass_barycenter = HourglassBarycenter()
        self.ash_twin             = AshTwin(self.hourglass_barycenter)
        self.ember_twin           = EmberTwin(self.hourglass_barycenter)
        self.timber_hearth        = TimberHearth()
        self.attlerock       = Attlerock(self.timber_hearth)
        self.brittle_hollow  = BrittleHollow()
        self.hollows_lantern = HollowsLantern(self.brittle_hollow)
        self.giants_deep     = GiantsDeep()
        self.dark_bramble    = DarkBramble()
        self.interloper      = Interloper()

        # Keep in update order (parents strictly before their children)
        self._bodies = [
            self.sun,
            self.sun_station,
            self.hourglass_barycenter,   # must come before the twins
            self.ash_twin,
            self.ember_twin,
            self.timber_hearth,
            self.attlerock,
            self.brittle_hollow,
            self.hollows_lantern,
            self.giants_deep,
            self.dark_bramble,
            self.interloper,
        ]

        for body in self._bodies:
            self.addItem(body)

        # Connect click signals (placeholder — panels attached in window.py)
        for body in self._bodies:
            body.clicked.connect(self._on_body_clicked)

    def _build_overlay(self) -> None:
        self._status_item = QGraphicsTextItem("")
        self._status_item.setFont(QFont("Consolas", 11))
        self._status_item.setDefaultTextColor(QColor(200, 180, 255, 170))
        self._status_item.setZValue(10)
        self.addItem(self._status_item)

        self._hint_item = QGraphicsTextItem("Click a planet to configure")
        self._hint_item.setFont(QFont("Consolas", 9))
        self._hint_item.setDefaultTextColor(QColor(160, 140, 200, 120))
        self._hint_item.setZValue(10)
        self.addItem(self._hint_item)
        br = self._hint_item.boundingRect()
        self._hint_item.setPos(-br.width() / 2, 62)

        self._update_status_display()

    # ── timer state interface (called from MainWindow) ─────────────────

    def set_timer_state(self, state: str) -> None:
        self._timer_state = state
        self._update_status_display()

    def set_remaining(self, secs: float) -> None:
        self._remaining_sec = secs
        self._update_status_display()

    def set_evolution(self, progress: float) -> None:
        self._evolution_progress = progress

    def trigger_supernova(self) -> None:
        """Placeholder: briefly show session-complete message."""
        self._timer_state = "supernova"
        self._update_status_display()

    def _fmt_time(self, secs: float) -> str:
        s = max(0, int(secs))
        return f"{s // 60:02d}:{s % 60:02d}"

    def _update_status_display(self) -> None:
        state = self._timer_state
        if state == "idle":
            text = "Space: start  |  right-click: menu"
        elif state == "focus":
            text = f"FOCUS  {self._fmt_time(self._remaining_sec)}"
        elif state == "short_break":
            text = f"SHORT BREAK  {self._fmt_time(self._remaining_sec)}"
        elif state == "long_break":
            text = f"LONG BREAK  {self._fmt_time(self._remaining_sec)}"
        elif state == "paused":
            text = f"PAUSED  {self._fmt_time(self._remaining_sec)}"
        elif state == "supernova":
            text = "Loop complete!"
        else:
            text = ""

        self._status_item.setPlainText(text)
        br = self._status_item.boundingRect()
        self._status_item.setPos(-br.width() / 2, SCENE_R * 0.74)
        self._hint_item.setVisible(self._timer_state == "idle")

    def _start_loop(self) -> None:
        self._timer = QTimer(self)
        self._timer.setInterval(16)   # ~60 fps
        self._timer.timeout.connect(self._tick)
        self._timer.start()
        self._last_t = time.monotonic()

    # ── animation loop ────────────────────────────────────────────────

    def _tick(self) -> None:
        now = time.monotonic()
        dt  = min(now - self._last_t, 0.05)   # cap at 50 ms (lag guard)
        self._last_t = now
        for body in self._bodies:
            body.advance(dt)

    # ── interaction ───────────────────────────────────────────────────

    def _on_body_clicked(self, name: str) -> None:
        self.body_clicked.emit(name)

    def set_clickable(self, enabled: bool) -> None:
        for body in self._bodies:
            body.set_clickable(enabled)

    # ── background rendering ──────────────────────────────────────────

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Punch the entire rect to transparent first — corners outside the circle
        # will stay see-through (desktop visible) thanks to WA_TranslucentBackground.
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(rect, Qt.GlobalColor.transparent)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

        # Dark space tint — evenly-spaced stops so Qt interpolates smoothly;
        # alpha decreases steadily from centre (~90 %) to a fully-transparent rim.
        bg = QRadialGradient(QPointF(0, 0), SCENE_R)
        bg.setColorAt(0.00, QColor(22, 10, 46, 232))
        bg.setColorAt(0.18, QColor(19,  8, 40, 212))
        bg.setColorAt(0.36, QColor(15,  6, 32, 182))
        bg.setColorAt(0.52, QColor(11,  5, 24, 148))
        bg.setColorAt(0.66, QColor( 7,  3, 16, 108))
        bg.setColorAt(0.78, QColor( 4,  2, 10,  68))
        bg.setColorAt(0.88, QColor( 2,  1,  5,  34))
        bg.setColorAt(0.95, QColor( 1,  0,  2,  10))
        bg.setColorAt(1.00, QColor( 0,  0,  0,   0))
        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(0, 0), float(SCENE_R), float(SCENE_R))

        # Orbit guide rings
        pen = QPen(QColor(85, 85, 130, 65))
        pen.setWidthF(0.8)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for r in self._CIRCULAR_ORBITS:
            painter.drawEllipse(QPointF(0, 0), float(r), float(r))

        # Interloper's elliptical orbit ring
        cx = Interloper.CENTER_X
        a  = Interloper.SEMI_MAJOR
        b  = Interloper.SEMI_MINOR
        painter.drawEllipse(QRectF(cx - a, -b, 2 * a, 2 * b))


class SolarSystemView(QGraphicsView):

    context_menu_requested = pyqtSignal()

    def __init__(self, scene: SolarSystemScene) -> None:
        super().__init__(scene)
        self._drag_pos = None

        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(self.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setBackgroundBrush(QBrush(Qt.BrushStyle.NoBrush))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # ── Fit scene to view on resize + initial show ────────────────────

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # Delay to ensure widget has its final size before fitting
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self._fit)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit()

    def _fit(self) -> None:
        if self.scene():
            self.fitInView(self.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    # ── Drag-to-move window (click on empty space) ────────────────────

    def mousePressEvent(self, event) -> None:
        item = self.itemAt(event.pos())
        if item is None and event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            )
        else:
            self._drag_pos = None
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event) -> None:
        self.context_menu_requested.emit()
        event.accept()
