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
from .bodies.ash_twin       import AshTwin, EmberTwin
from .bodies.timber_hearth  import TimberHearth, Attlerock
from .bodies.brittle_hollow import BrittleHollow, HollowsLantern
from .bodies.giants_deep    import GiantsDeep
from .bodies.dark_bramble   import DarkBramble
from .bodies.interloper     import Interloper

SCENE_R = 330   # half-width of the scene bounding box


class SolarSystemScene(QGraphicsScene):

    # Main circular orbit radii to draw as guide rings
    _CIRCULAR_ORBITS = [60, 100, 150, 200, 245, 285]

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
        self.sun             = Sun()
        self.sun_station     = SunStation()
        self.ash_twin        = AshTwin()
        self.ember_twin      = EmberTwin(self.ash_twin)
        self.timber_hearth   = TimberHearth()
        self.attlerock       = Attlerock(self.timber_hearth)
        self.brittle_hollow  = BrittleHollow()
        self.hollows_lantern = HollowsLantern(self.brittle_hollow)
        self.giants_deep     = GiantsDeep()
        self.dark_bramble    = DarkBramble()
        self.interloper      = Interloper()

        # Keep in update order (parents strictly before their moons)
        self._bodies = [
            self.sun,
            self.sun_station,
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

        # Dark space circle
        bg = QRadialGradient(QPointF(0, 0), SCENE_R)
        bg.setColorAt(0.0, QColor(18,  8, 35, 235))
        bg.setColorAt(0.6, QColor(10,  4, 22, 235))
        bg.setColorAt(1.0, QColor( 4,  2, 10, 200))
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
        # Solid black fill — scene drawBackground paints the dark space circle on top
        self.setStyleSheet("background-color: #000000; border: none;")
        self.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

    # ── Fit scene to view on resize ───────────────────────────────────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
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
