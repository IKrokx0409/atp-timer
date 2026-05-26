import math
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QRadialGradient, QColor, QBrush
from .base_body import BaseBody

_YELLOW      = QColor(255, 225, 60)
_CORONA_MID  = QColor(255, 180, 30)
_CORONA_OUT  = QColor(255, 120, 10)


class Sun(BaseBody):
    """Central star — pulsing glow, no orbit."""

    _R = 22   # sphere radius

    def __init__(self) -> None:
        super().__init__(
            name="Sun",
            color=_YELLOW,
            radius=self._R,
            orbit_radius=0,
            orbit_speed=0,
        )
        self._elapsed = 0.0
        self._clickable = False   # Sun is not a settings planet
        self.setZValue(3)

    # Sun never orbits but we still need to update the glow pulse
    def advance(self, dt: float) -> None:
        self._elapsed += dt
        self.update()   # schedule repaint

    def boundingRect(self) -> QRectF:
        r = self._R + 22    # room for outer glow
        return QRectF(-r, -r, r * 2, r * 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pulse = 1.0 + 0.12 * math.sin(self._elapsed * 1.8)

        # --- outer corona ---
        r_out = (self._R + 18) * pulse
        g_out = QRadialGradient(0, 0, r_out)
        g_out.setColorAt(0.0, QColor(255, 160, 20, 50))
        g_out.setColorAt(0.5, QColor(255, 120, 10, 20))
        g_out.setColorAt(1.0, QColor(255,  80,  0,  0))
        painter.setBrush(QBrush(g_out))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(-r_out, -r_out, r_out * 2, r_out * 2))

        # --- inner halo ---
        r_mid = (self._R + 8) * pulse
        g_mid = QRadialGradient(0, 0, r_mid)
        g_mid.setColorAt(0.0, QColor(255, 210, 60, 120))
        g_mid.setColorAt(1.0, QColor(255, 150, 30,   0))
        painter.setBrush(QBrush(g_mid))
        painter.drawEllipse(QRectF(-r_mid, -r_mid, r_mid * 2, r_mid * 2))

        # --- main sphere ---
        self._paint_sphere(painter)
