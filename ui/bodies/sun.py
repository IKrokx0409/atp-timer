import math
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QRadialGradient, QColor, QBrush
from .base_body import BaseBody

_YELLOW = QColor(255, 225, 60)


class Sun(BaseBody):
    """Central star — dominant presence, pulsing glow."""

    _R = 48   # sphere radius — Sun dominates the scene

    def __init__(self) -> None:
        super().__init__(
            name="Sun",
            color=_YELLOW,
            radius=self._R,
            orbit_radius=0,
            orbit_speed=0,
        )
        self._elapsed = 0.0
        self._clickable = False
        self.setZValue(3)

    def advance(self, dt: float) -> None:
        self._elapsed += dt
        self.update()

    def boundingRect(self) -> QRectF:
        r = self._R + 28
        return QRectF(-r, -r, r * 2, r * 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pulse = 1.0 + 0.10 * math.sin(self._elapsed * 1.6)

        # Outer diffuse corona
        r_out = (self._R + 24) * pulse
        g_out = QRadialGradient(0, 0, r_out)
        g_out.setColorAt(0.0, QColor(255, 160, 20, 55))
        g_out.setColorAt(0.5, QColor(255, 120, 10, 22))
        g_out.setColorAt(1.0, QColor(255,  80,  0,  0))
        painter.setBrush(QBrush(g_out))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(-r_out, -r_out, r_out * 2, r_out * 2))

        # Inner halo
        r_mid = (self._R + 10) * pulse
        g_mid = QRadialGradient(0, 0, r_mid)
        g_mid.setColorAt(0.0, QColor(255, 210, 60, 130))
        g_mid.setColorAt(1.0, QColor(255, 150, 30,   0))
        painter.setBrush(QBrush(g_mid))
        painter.drawEllipse(QRectF(-r_mid, -r_mid, r_mid * 2, r_mid * 2))

        # Main sphere
        self._paint_sphere(painter)
