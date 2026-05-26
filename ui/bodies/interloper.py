"""
The Interloper — icy comet with an elongated elliptical orbit.

  x = CENTER_X + SEMI_MAJOR * cos(θ)
  y =             SEMI_MINOR * sin(θ)

At θ=π (left): closest approach to Sun (~190px)
At θ=0 (right): apoapsis (~314px)
"""
import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class Interloper(BaseBody):

    CENTER_X   = 62
    SEMI_MAJOR = 252
    SEMI_MINOR = 90

    def __init__(self) -> None:
        super().__init__(
            name="The Interloper",
            color=QColor(192, 212, 232),
            radius=8,
            orbit_radius=0,
            orbit_speed=math.tau / 490,
            start_angle=math.radians(90),
        )

    def _recalc_pos(self) -> None:
        x = self.CENTER_X + self.SEMI_MAJOR * math.cos(self.angle)
        y = self.SEMI_MINOR * math.sin(self.angle)
        self.setPos(x, y)
