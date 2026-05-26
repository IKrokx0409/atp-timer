"""
BaseBody — base class for every celestial body in the solar system.

Coordinate system
-----------------
The scene origin (0, 0) is the Sun's centre.
Each body stores its current orbital angle and recomputes its scene
position every frame via advance(dt).

Moons pass their parent BaseBody; they read parent.pos() (scene coords)
so parents must be advanced BEFORE their children each tick.
"""

import math
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QRadialGradient, QColor, QBrush, QPainterPath
from PyQt6.QtWidgets import QGraphicsObject


class BaseBody(QGraphicsObject):
    """Clickable, animated celestial body placeholder (coloured sphere)."""

    clicked = pyqtSignal(str)   # emits self.name when clicked in setup mode

    def __init__(
        self,
        name: str,
        color: QColor,
        radius: float,          # visual sphere radius, scene units
        orbit_radius: float,    # distance from parent centre (0 for Sun)
        orbit_speed: float,     # radians / second
        start_angle: float = 0.0,
        parent_body=None,       # BaseBody | None  (NOT a Qt parent)
    ) -> None:
        super().__init__()

        self.name         = name
        self.color        = color
        self.radius       = radius
        self.orbit_radius = orbit_radius
        self.orbit_speed  = orbit_speed
        self.angle        = start_angle
        self.parent_body  = parent_body

        self._clickable   = True   # disabled when timer is running

        self.setZValue(2)
        self.setAcceptHoverEvents(True)
        self._recalc_pos()

    # ── Qt abstract interface ─────────────────────────────────────────

    def boundingRect(self) -> QRectF:
        r = self.radius + 4   # small padding for glow / anti-alias
        return QRectF(-r, -r, r * 2, r * 2)

    def shape(self) -> QPainterPath:
        """Circular hit-test area (not the full bounding rect)."""
        path = QPainterPath()
        r = self.radius
        path.addEllipse(QRectF(-r, -r, r * 2, r * 2))
        return path

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._paint_sphere(painter)

    # ── Sphere rendering ──────────────────────────────────────────────

    def _paint_sphere(self, painter: QPainter) -> None:
        """3-D looking sphere via off-centre radial gradient."""
        r = self.radius
        # Light source at upper-left
        gradient = QRadialGradient(-r * 0.35, -r * 0.35, r * 1.65)
        gradient.setColorAt(0.00, self.color.lighter(170))
        gradient.setColorAt(0.45, self.color)
        gradient.setColorAt(1.00, self.color.darker(215))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(-r, -r, r * 2, r * 2))

    # ── Animation ─────────────────────────────────────────────────────

    def advance(self, dt: float) -> None:
        """Move the body forward by dt seconds along its orbit."""
        self.angle += self.orbit_speed * dt
        self._recalc_pos()

    def _recalc_pos(self) -> None:
        if self.parent_body is not None:
            p = self.parent_body.pos()
            cx, cy = p.x(), p.y()
        else:
            cx = cy = 0.0
        self.setPos(
            cx + self.orbit_radius * math.cos(self.angle),
            cy + self.orbit_radius * math.sin(self.angle),
        )

    # ── Clickability ──────────────────────────────────────────────────

    def set_clickable(self, value: bool) -> None:
        self._clickable = value
        self.setAcceptedMouseButtons(
            Qt.MouseButton.LeftButton if value else Qt.MouseButton.NoButton
        )

    def mousePressEvent(self, event) -> None:
        if self._clickable and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.name)
        else:
            super().mousePressEvent(event)
