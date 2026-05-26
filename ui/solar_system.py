"""
SolarSystemScene  — QGraphicsScene that owns and animates all bodies.
SolarSystemView   — QGraphicsView wrapper; handles drag-to-move and fitInView.

Scene coordinate space: sun at (0, 0), radius ~330 units.
"""

import time
from PyQt6.QtCore  import Qt, QRectF, QPointF, QTimer
from PyQt6.QtGui   import QPainter, QColor, QPen, QBrush, QRadialGradient
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView

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

    # Circular orbit guide rings (one per main-body orbit)
    _CIRCULAR_ORBITS = [82, 118, 182, 245, 292, 328]

    def __init__(self) -> None:
        super().__init__()
        self.setSceneRect(-SCENE_R, -SCENE_R, SCENE_R * 2, SCENE_R * 2)

        self._last_t: float | None = None
        self._bodies: list = []

        self._build()
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
        # Placeholder: print to console until panels are wired up
        print(f"[click] {name}")

    def set_clickable(self, enabled: bool) -> None:
        for body in self._bodies:
            body.set_clickable(enabled)

    # ── background rendering ──────────────────────────────────────────

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill entire exposed rect first (corners outside the circle)
        painter.fillRect(rect, QColor(0, 0, 0))

        # Dark space circle — slightly lighter centre so it's distinct from the pure-black border
        bg = QRadialGradient(QPointF(0, 0), SCENE_R)
        bg.setColorAt(0.0, QColor(28, 12, 55))
        bg.setColorAt(0.7, QColor(14,  6, 30))
        bg.setColorAt(1.0, QColor( 6,  2, 14))
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
