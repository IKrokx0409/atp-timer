import math
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QPainter
from .base_body import BaseBody


class HourglassBarycenter(BaseBody):
    """
    Invisible barycenter of the Hourglass Twins binary system.
    Orbits the Sun; both twins use this as their parent_body.
    Not clickable, not rendered.
    """

    def __init__(self) -> None:
        super().__init__(
            name="_hourglass_barycenter",
            color=QColor(0, 0, 0, 0),
            radius=1,
            orbit_radius=100,
            orbit_speed=math.tau / 80,   # barycenter period ≈ 80 s
            start_angle=math.radians(30),
        )
        self._clickable = False
        self.setZValue(0)

    def boundingRect(self) -> QRectF:
        return QRectF(-1, -1, 2, 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        pass  # invisible — just a position anchor


class AshTwin(BaseBody):
    """Sandy planet — hosts the Ash Twin Towers. Orbits the shared barycenter."""

    def __init__(self, barycenter: HourglassBarycenter) -> None:
        super().__init__(
            name="Ash Twin",
            color=QColor(200, 162, 100),
            radius=14,
            orbit_radius=22,             # distance from barycenter
            orbit_speed=math.tau / 22,   # binary spin period ≈ 22 s
            start_angle=0.0,
            parent_body=barycenter,
        )


class EmberTwin(BaseBody):
    """Volcanic binary partner. Always opposite Ash Twin around the barycenter."""

    def __init__(self, barycenter: HourglassBarycenter) -> None:
        super().__init__(
            name="Ember Twin",
            color=QColor(215, 92, 42),
            radius=10,
            orbit_radius=22,             # equal distance (symmetric binary)
            orbit_speed=math.tau / 22,   # same period as Ash Twin
            start_angle=math.radians(180),  # exactly opposite
            parent_body=barycenter,
        )
