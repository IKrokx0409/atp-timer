"""
The Interloper — icy comet with an elongated elliptical orbit.

Ellipse equation (scene coords, sun at origin):
  x = CENTER_X + SEMI_MAJOR * cos(θ)
  y =             SEMI_MINOR * sin(θ)

At θ = π  (left side):  x ≈ CENTER_X − SEMI_MAJOR  → closest to sun
At θ = 0  (right side): x ≈ CENTER_X + SEMI_MAJOR  → apoapsis
"""

import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class Interloper(BaseBody):

    CENTER_X   = 70     # scene units — ellipse centre offset from sun
    SEMI_MAJOR = 240    # 'a' (horizontal half-extent)
    SEMI_MINOR = 85     # 'b' (vertical half-extent)

    def __init__(self) -> None:
        super().__init__(
            name="The Interloper",
            color=QColor(192, 212, 232),
            radius=9,
            orbit_radius=0,            # unused — overridden below
            orbit_speed=math.tau / 480,  # period ≈ 480 s
            start_angle=math.radians(90),
        )

    def _recalc_pos(self) -> None:
        """Parametric ellipse instead of circle."""
        x = self.CENTER_X + self.SEMI_MAJOR * math.cos(self.angle)
        y = self.SEMI_MINOR * math.sin(self.angle)
        self.setPos(x, y)
