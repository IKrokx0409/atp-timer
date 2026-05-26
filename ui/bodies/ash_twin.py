import math
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QPainter
from .base_body import BaseBody


class HourglassBarycenter(BaseBody):
    """
    Invisible barycenter of the Hourglass Twins binary system.
    Orbits the Sun; both twins use this as their parent_body.
    """

    def __init__(self) -> None:
        super().__init__(
            name="_hourglass_barycenter",
            color=QColor(0, 0, 0, 0),
            radius=1,
            orbit_radius=118,
            orbit_speed=math.tau / 85,
            start_angle=math.radians(30),
        )
        self._clickable = False
        self.setZValue(0)

    def boundingRect(self) -> QRectF:
        return QRectF(-1, -1, 2, 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        pass  # invisible


class AshTwin(BaseBody):
    """Sandy planet — hosts the Ash Twin Towers."""

    def __init__(self, barycenter: HourglassBarycenter) -> None:
        super().__init__(
            name="Ash Twin",
            color=QColor(200, 162, 100),
            radius=16,
            orbit_radius=22,
            orbit_speed=math.tau / 22,
            start_angle=0.0,
            parent_body=barycenter,
        )


class EmberTwin(BaseBody):
    """Volcanic binary partner — always opposite Ash Twin."""

    def __init__(self, barycenter: HourglassBarycenter) -> None:
        super().__init__(
            name="Ember Twin",
            color=QColor(215, 92, 42),
            radius=13,
            orbit_radius=22,
            orbit_speed=math.tau / 22,
            start_angle=math.radians(180),
            parent_body=barycenter,
        )
